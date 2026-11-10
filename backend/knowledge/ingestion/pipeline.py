import logging
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from knowledge.ingestion.base import IngestionItem
from knowledge.ingestion.license_checker import MODE_EVIDENCE_ONLY, LicenseChecker
from knowledge.ingestion.normalize import best_supporting_passage, claim_hash, content_hash, normalize_document_text
from knowledge.models import Evidence, ExtractedClaim, Source, SourceDocument
from knowledge.tasks import embed_evidence_task
from verification.services.claim_extraction import ClaimExtractionService
from verification.services.claim_verification import ClaimVerificationService

logger = logging.getLogger(__name__)

STATE_STORED = "stored"
STATE_CLAIMS_EXTRACTED = "claims_extracted"
STATE_VERIFIED = "verified"
STATE_NO_CLAIMS = "no_claims"
STATE_EVIDENCE_ONLY = "evidence_only"
COMPLETE_STATES = {STATE_VERIFIED, STATE_NO_CLAIMS, STATE_EVIDENCE_ONLY}


class InsufficientContentError(ValueError):
    """The fetched document has too little text to be a knowledge import."""


class ExternalIngestionPipeline:
    def __init__(self, extractor=None, verifier=None):
        self.extractor = extractor or ClaimExtractionService()
        self.verifier = verifier or ClaimVerificationService()

    def ingest_item(
        self,
        item: IngestionItem,
        target_claim_for_evidence: ExtractedClaim | None = None,
        *,
        defer_flashcards: bool = False,
        topic_concept_id: int | None = None,
    ) -> dict:
        # 1. License and policy gate check (every source, fail closed).
        decision = LicenseChecker.evaluate(item)

        normalized = normalize_document_text(item.raw_text)
        min_chars = int(getattr(settings, "INGESTION_MIN_DOCUMENT_CHARS", 30))
        if len(normalized) < min_chars:
            raise InsufficientContentError(
                f"'{item.url}' has {len(normalized)} characters of text (minimum {min_chars})."
            )
        digest = content_hash(item.raw_text)
        metadata = {**item.metadata, "policy": decision.as_metadata(item), "ingestion_state": STATE_STORED}
        if topic_concept_id:
            metadata["topic_concept_id"] = topic_concept_id

        # 2-3. Source + versioned document. Short transaction, no network calls.
        with transaction.atomic():
            source, _ = Source.objects.get_or_create(
                name=item.source_name,
                defaults={
                    "domain": item.source_domain,
                    "source_type": item.source_type,
                    "authority_score": item.authority_score,
                    "license": item.license_name,
                    "license_url": item.license_url,
                    "attribution_required": item.attribution_required,
                    "commercial_use_allowed": item.commercial_use_allowed,
                    "ai_use_allowed": item.ai_use_allowed,
                    "scraping_allowed": item.scraping_allowed,
                    "api_available": True,
                    "access_method": "api",
                },
            )
            current = (
                SourceDocument.objects.select_for_update()
                .filter(source=source, url=item.url, is_current=True)
                .first()
            )
            version = "new"
            if current is not None:
                current_hash = current.content_hash or content_hash(current.raw_text)
                if current_hash == digest:
                    if not current.content_hash:
                        current.content_hash = current_hash
                        current.save(update_fields=["content_hash"])
                    state = (current.metadata or {}).get("ingestion_state")
                    # Legacy documents (no state) were processed in one transaction.
                    if state is None or state in COMPLETE_STATES:
                        return {"source": source, "document": current, "claims": [], "verification_results": [],
                                "mode": "already_ingested", "policy": decision}
                    document, version = current, "resumed"
                else:
                    # Content changed: keep the old version (and its knowledge) for
                    # provenance, and process the new text as the current version.
                    current.is_current = False
                    current.save(update_fields=["is_current"])
                    version = "updated"
            if version != "resumed":
                document = SourceDocument.objects.create(
                    source=source, uploaded_note=None, title=item.title[:255],
                    document_type=item.document_type, url=item.url, raw_text=item.raw_text,
                    metadata=metadata, retrieved_at=timezone.now(),
                    external_id=item.external_id, content_hash=digest, is_current=True,
                )
                if current is not None:
                    current.superseded_by = document
                    current.save(update_fields=["superseded_by"])

        # 4. Evidence-only path (e.g. Reddit or auxiliary evidence link)
        if decision.mode == MODE_EVIDENCE_ONLY or target_claim_for_evidence is not None:
            may_embed = decision.policy.ai_use and item.ai_use_allowed
            evidence_records = []
            with transaction.atomic():
                if target_claim_for_evidence:
                    evidence = Evidence.objects.create(
                        claim=target_claim_for_evidence,
                        source=source,
                        relation=Evidence.RELATED,
                        title=item.title[:255],
                        url=item.url,
                        excerpt=item.raw_text[:1000],
                        relevance_score=0.50,
                        retrieved_at=timezone.now(),
                    )
                    evidence_records.append(evidence)
                    if may_embed:
                        transaction.on_commit(lambda eid=evidence.id: embed_evidence_task.delay(eid))
                self._set_state(document, STATE_EVIDENCE_ONLY)

            return {
                "source": source,
                "document": document,
                "claims": [],
                "evidence": evidence_records,
                "mode": "evidence_only",
                "policy": decision,
                "document_version": version,
            }

        # 5. Full Ingestion: Extract claims -> Run verification -> Canonicalize
        existing_claims = list(document.extracted_claims.all()) if version == "resumed" else []
        if existing_claims:
            created_claims = [c for c in existing_claims if c.status == ExtractedClaim.STATUS_PENDING]
        else:
            # LLM call outside any transaction.
            claim_texts = self.extractor.extract_claims(item.raw_text)
            created_claims = self._store_claims(document, source, item, decision, claim_texts)
            if not created_claims:
                self._set_state(document, STATE_NO_CLAIMS)
                return {"source": source, "document": document, "claims": [], "verification_results": [],
                        "mode": "no_claims", "policy": decision, "document_version": version}

        verification_results = []
        for claim in created_claims:
            if defer_flashcards:
                res = self.verifier.verify_claim(claim, defer_flashcard=True)
            else:
                res = self.verifier.verify_claim(claim)
            verification_results.append(res)
        self._set_state(document, STATE_VERIFIED)

        return {
            "source": source,
            "document": document,
            "claims": created_claims,
            "verification_results": verification_results,
            "mode": "canonical_knowledge",
            "policy": decision,
            "document_version": version,
        }

    @staticmethod
    def _set_state(document: SourceDocument, state: str) -> None:
        document.metadata = {**(document.metadata or {}), "ingestion_state": state}
        document.save(update_fields=["metadata"])

    def _store_claims(self, document, source, item, decision, claim_texts) -> list[ExtractedClaim]:
        min_coverage = float(getattr(settings, "INGESTION_GROUNDING_MIN_COVERAGE", 0.75))
        attest = decision.policy.self_attestation and item.authority_score >= Decimal("0.70")
        seen_hashes = set()
        created_claims = []
        with transaction.atomic():
            for text in claim_texts:
                text = (text or "").strip()
                digest = claim_hash(text)
                if not text or digest in seen_hashes:
                    continue
                seen_hashes.add(digest)
                claim = ExtractedClaim.objects.create(
                    source_document=document,
                    text=text,
                )
                if attest:
                    # The source supports a claim only if the claim is actually
                    # grounded in a passage of the source (not hallucinated).
                    coverage, passage = best_supporting_passage(text, item.raw_text)
                    if coverage >= min_coverage:
                        evidence = Evidence.objects.create(
                            claim=claim,
                            source=source,
                            relation=Evidence.SUPPORTS,
                            title=item.title[:255],
                            url=item.url,
                            excerpt=passage[:1000],
                            relevance_score=Decimal("0.90"),
                            retrieved_at=timezone.now(),
                        )
                        transaction.on_commit(lambda eid=evidence.id: embed_evidence_task.delay(eid))
                    else:
                        logger.info(
                            "ingestion.attestation.ungrounded document=%s coverage=%.2f", document.id, coverage,
                        )
                created_claims.append(claim)
            if created_claims:
                document.metadata = {**(document.metadata or {}), "ingestion_state": STATE_CLAIMS_EXTRACTED}
                document.save(update_fields=["metadata"])
        return created_claims
