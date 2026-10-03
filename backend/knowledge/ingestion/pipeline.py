from django.db import transaction
from django.utils import timezone
from knowledge.ingestion.base import IngestionItem
from knowledge.ingestion.license_checker import LicenseChecker
from knowledge.models import Evidence, ExtractedClaim, Source, SourceDocument
from knowledge.tasks import embed_evidence_task
from verification.services.claim_extraction import ClaimExtractionService
from verification.services.claim_verification import ClaimVerificationService


class ExternalIngestionPipeline:
    def __init__(self, extractor=None, verifier=None):
        self.extractor = extractor or ClaimExtractionService()
        self.verifier = verifier or ClaimVerificationService()

    @transaction.atomic
    def ingest_item(self, item: IngestionItem, target_claim_for_evidence: ExtractedClaim | None = None) -> dict:
        # 1. License and policy gate check
        LicenseChecker.validate(item)

        # 2. Get or create Source entity
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
            },
        )

        # 3. Create SourceDocument (uploaded_note remains None)
        document = SourceDocument.objects.create(
            source=source,
            uploaded_note=None,
            title=item.title,
            document_type=item.document_type,
            url=item.url,
            raw_text=item.raw_text,
            metadata=item.metadata,
            retrieved_at=timezone.now(),
        )

        # 4. Evidence-only path (e.g. Reddit or auxiliary evidence link)
        if item.evidence_only or target_claim_for_evidence is not None:
            evidence_records = []
            if target_claim_for_evidence:
                evidence = Evidence.objects.create(
                    claim=target_claim_for_evidence,
                    source=source,
                    relation=Evidence.RELATED,
                    title=item.title,
                    url=item.url,
                    excerpt=item.raw_text[:1000],
                    relevance_score=0.50,
                )
                evidence_records.append(evidence)
                transaction.on_commit(lambda eid=evidence.id: embed_evidence_task.delay(eid))

            return {
                "source": source,
                "document": document,
                "claims": [],
                "evidence": evidence_records,
                "mode": "evidence_only",
            }

        # 5. Full Ingestion: Extract claims -> Run verification -> Canonicalize
        claim_texts = self.extractor.extract_claims(item.raw_text)
        created_claims = []
        for text in claim_texts:
            claim = ExtractedClaim.objects.create(
                source_document=document,
                text=text,
            )
            created_claims.append(claim)

        verification_results = []
        for claim in created_claims:
            res = self.verifier.verify_claim(claim)
            verification_results.append(res)

        return {
            "source": source,
            "document": document,
            "claims": created_claims,
            "verification_results": verification_results,
            "mode": "canonical_knowledge",
        }