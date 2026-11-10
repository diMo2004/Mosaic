"""Source-policy enforcement for every external ingestion item.

Permissions are tracked separately for each dimension that matters to MOSAIC:

* retrieval  - may we fetch it automatically (API terms / robots.txt)?
* ai_use     - may the text be sent to an LLM for claim extraction/embedding?
* commercial - does the license permit commercial use?
* redistribution - may derived cards be shown publicly, and on what terms?
* attribution - what notice must accompany derived material?

Policies come from a reviewed registry (``SOURCE_POLICIES``), never from the
domain alone: an item must also declare a license that its policy accepts.
Unknown sources, unknown licenses, and sources whose terms have not been
cleared fail closed. Summary of the reviewed terms: docs/source_policy.md.
"""
from dataclasses import dataclass, field

from django.conf import settings

from knowledge.ingestion.base import IngestionItem


class LicensePolicyError(RuntimeError):
    """Raised when an external source fails licensing or AI-use policies."""
    pass


STATUS_APPROVED = "approved"
# Terms are restrictive or unclear; blocked until a documented review lists the
# key in settings.INGESTION_REVIEWED_SOURCES.
STATUS_REQUIRES_REVIEW = "requires_review"

MODE_CANONICAL = "canonical"
MODE_EVIDENCE_ONLY = "evidence_only"

REDISTRIBUTION_SHARE_ALIKE = "share_alike_with_attribution"
REDISTRIBUTION_ATTRIBUTION = "attribution"
REDISTRIBUTION_PUBLIC_DOMAIN = "public_domain"
REDISTRIBUTION_LINK_ONLY = "link_only"


@dataclass(frozen=True)
class SourcePolicy:
    key: str
    domains: tuple[str, ...]
    licenses: frozenset[str]
    status: str = STATUS_APPROVED
    mode: str = MODE_CANONICAL
    ai_use: bool = True
    commercial: bool = True
    redistribution: str = REDISTRIBUTION_ATTRIBUTION
    # May a claim extracted from this source count as supported by the source
    # itself (after a grounding check)? Only for curated reference material.
    self_attestation: bool = False
    terms_url: str = ""
    notes: str = ""
    requires_settings: tuple[str, ...] = field(default_factory=tuple)

    def matches_domain(self, domain: str) -> bool:
        domain = (domain or "").lower()
        return any(domain == d or domain.endswith("." + d) for d in self.domains)


PERMISSIVE_CODE_LICENSES = frozenset({
    "mit", "apache-2.0", "bsd-2-clause", "bsd-3-clause", "isc", "0bsd",
    "unlicense", "cc0-1.0", "cc-by-4.0", "cc-by-sa-4.0",
})

SOURCE_POLICIES: dict[str, SourcePolicy] = {
    policy.key: policy
    for policy in [
        SourcePolicy(
            key="wikimedia",
            domains=("en.wikipedia.org",),
            licenses=frozenset({"cc-by-sa-4.0", "cc-by-sa-3.0"}),
            redistribution=REDISTRIBUTION_SHARE_ALIKE,
            self_attestation=True,
            terms_url="https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use",
        ),
        SourcePolicy(
            key="arxiv",
            domains=("arxiv.org",),
            # Descriptive metadata (title, abstract, authors) is CC0 under the
            # arXiv API terms. Full-text e-prints are NOT covered and are never fetched.
            licenses=frozenset({"cc0-1.0"}),
            redistribution=REDISTRIBUTION_PUBLIC_DOMAIN,
            self_attestation=False,  # preprints are not peer reviewed
            terms_url="https://info.arxiv.org/help/api/tou.html",
        ),
        SourcePolicy(
            key="github",
            domains=("github.com",),
            licenses=PERMISSIVE_CODE_LICENSES,
            self_attestation=False,  # READMEs describe a project, not general CS facts
            terms_url="https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
        ),
        SourcePolicy(
            key="stackexchange",
            domains=("stackoverflow.com", "stackexchange.com", "superuser.com", "serverfault.com", "askubuntu.com"),
            licenses=frozenset({"cc-by-sa-2.5", "cc-by-sa-3.0", "cc-by-sa-4.0"}),
            redistribution=REDISTRIBUTION_SHARE_ALIKE,
            terms_url="https://stackexchange.com/legal/api-terms-of-use",
            notes="Show Stack Exchange as source, author name and post link.",
        ),
        SourcePolicy(
            key="reddit",
            domains=("reddit.com",),
            licenses=frozenset({"reddit-data-api-terms"}),
            mode=MODE_EVIDENCE_ONLY,
            # Reddit Data API terms prohibit using user content to train AI
            # models and require a separate agreement for commercial use.
            ai_use=False,
            commercial=False,
            redistribution=REDISTRIBUTION_LINK_ONLY,
            terms_url="https://redditinc.com/policies/data-api-terms",
            requires_settings=("REDDIT_LEGAL_REVIEW_APPROVED",),
        ),
        SourcePolicy(
            key="official_docs:python",
            domains=("docs.python.org",),
            licenses=frozenset({"psf-2.0"}),
            self_attestation=True,
            terms_url="https://docs.python.org/3/license.html",
        ),
        SourcePolicy(
            key="official_docs:javascript",
            domains=("developer.mozilla.org",),
            licenses=frozenset({"cc-by-sa-2.5"}),
            redistribution=REDISTRIBUTION_SHARE_ALIKE,
            self_attestation=True,
            terms_url="https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Attrib_copyright_license",
            notes='Credit "Mozilla Contributors" with a link to the page.',
        ),
        SourcePolicy(
            key="official_docs:typescript",
            domains=("typescriptlang.org",),
            licenses=frozenset({"cc-by-4.0"}),
            self_attestation=True,
            terms_url="https://github.com/microsoft/TypeScript-Website",
        ),
        SourcePolicy(
            key="official_docs:java",
            domains=("docs.oracle.com",),
            licenses=frozenset({"oracle-documentation"}),
            status=STATUS_REQUIRES_REVIEW,
            commercial=False,
            redistribution=REDISTRIBUTION_LINK_ONLY,
            self_attestation=True,
            terms_url="https://docs.oracle.com/en/java/javase/21/docs/legal/copyright.html",
            notes="All rights reserved; reuse not licensed.",
        ),
        SourcePolicy(
            key="official_docs:cpp",
            domains=("isocpp.org",),
            licenses=frozenset({"isocpp-terms-of-use"}),
            status=STATUS_REQUIRES_REVIEW,
            commercial=False,
            redistribution=REDISTRIBUTION_LINK_ONLY,
            self_attestation=True,
            terms_url="https://isocpp.org/home/terms-of-use",
            notes="Copyright Standard C++ Foundation or authors; no public reuse license.",
        ),
    ]
}


@dataclass(frozen=True)
class PolicyDecision:
    policy: SourcePolicy
    license: str
    mode: str

    def as_metadata(self, item: IngestionItem) -> dict:
        return {
            "policy_key": self.policy.key,
            "mode": self.mode,
            "license": self.license,
            "license_url": item.license_url,
            "terms_url": self.policy.terms_url,
            "attribution_required": item.attribution_required,
            "attribution_text": item.attribution_text,
            "ai_use_allowed": self.policy.ai_use,
            "commercial_use_allowed": self.policy.commercial and item.commercial_use_allowed,
            "redistribution": self.policy.redistribution,
            "self_attestation": self.policy.self_attestation,
        }


def _reviewed_sources() -> set[str]:
    return {key.strip() for key in getattr(settings, "INGESTION_REVIEWED_SOURCES", []) if key.strip()}


def resolve_policy(item: IngestionItem) -> SourcePolicy | None:
    if item.policy_key:
        return SOURCE_POLICIES.get(item.policy_key)
    for policy in SOURCE_POLICIES.values():
        if policy.matches_domain(item.source_domain):
            return policy
    return None


def policy_for_adapter(policy_key: str) -> SourcePolicy | None:
    return SOURCE_POLICIES.get(policy_key)


def is_policy_enabled(policy: SourcePolicy) -> bool:
    if policy.status != STATUS_APPROVED and policy.key not in _reviewed_sources():
        return False
    return all(getattr(settings, name, False) is True for name in policy.requires_settings)


class LicenseChecker:
    @classmethod
    def evaluate(cls, item: IngestionItem) -> PolicyDecision:
        policy = resolve_policy(item)
        if policy is None:
            raise LicensePolicyError(
                f"No reviewed source policy covers '{item.source_domain}' "
                f"(policy_key={item.policy_key!r}); refusing to ingest."
            )
        if not policy.matches_domain(item.source_domain):
            raise LicensePolicyError(
                f"Domain '{item.source_domain}' is not covered by policy '{policy.key}'."
            )
        if policy.status != STATUS_APPROVED and policy.key not in _reviewed_sources():
            raise LicensePolicyError(
                f"Source policy '{policy.key}' requires a documented legal review "
                f"({policy.notes or policy.terms_url}). Add it to INGESTION_REVIEWED_SOURCES only after review."
            )
        for setting_name in policy.requires_settings:
            if getattr(settings, setting_name, False) is not True:
                raise LicensePolicyError(
                    f"Source policy '{policy.key}' is blocked until {setting_name}=True is configured "
                    "after legal review."
                )

        if policy.mode == MODE_EVIDENCE_ONLY and not item.evidence_only:
            raise LicensePolicyError(
                f"{policy.key} content cannot be ingested as direct knowledge. It is restricted to evidence only."
            )
        if policy.key == "reddit" and not item.metadata.get("legal_review_approved", False):
            raise LicensePolicyError(
                "Reddit ingestion is blocked pending legal review approval (flag 'legal_review_approved' missing)."
            )

        normalized_license = (item.license_name or "").strip().lower()
        if not normalized_license:
            raise LicensePolicyError(f"Item '{item.url}' declares no license; refusing to ingest.")
        if normalized_license not in policy.licenses:
            raise LicensePolicyError(
                f"License '{item.license_name}' is not accepted by source policy '{policy.key}'."
            )

        if not item.scraping_allowed:
            raise LicensePolicyError(f"Automated retrieval is not permitted for '{item.url}'.")
        # Canonical knowledge requires LLM claim extraction; evidence-only items
        # must not claim an AI permission the policy does not grant.
        if policy.mode == MODE_CANONICAL and not (policy.ai_use and item.ai_use_allowed):
            raise LicensePolicyError(f"AI processing is not permitted for '{item.url}'.")
        if item.ai_use_allowed and not policy.ai_use:
            raise LicensePolicyError(
                f"Item claims AI use is allowed but policy '{policy.key}' does not permit it."
            )

        if getattr(settings, "INGESTION_REQUIRE_COMMERCIAL_USE", False) and not (
            policy.commercial and item.commercial_use_allowed
        ):
            raise LicensePolicyError(
                f"Commercial use is not permitted for '{item.url}' and INGESTION_REQUIRE_COMMERCIAL_USE is enabled."
            )
        if policy.redistribution in (REDISTRIBUTION_SHARE_ALIKE, REDISTRIBUTION_ATTRIBUTION) and not item.attribution_required:
            raise LicensePolicyError(f"Policy '{policy.key}' requires attribution; item disables it.")

        mode = MODE_EVIDENCE_ONLY if item.evidence_only else policy.mode
        return PolicyDecision(policy=policy, license=normalized_license, mode=mode)

    @classmethod
    def validate(cls, item: IngestionItem) -> None:
        cls.evaluate(item)
