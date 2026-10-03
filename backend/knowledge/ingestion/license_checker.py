from knowledge.ingestion.base import IngestionItem

class LicensePolicyError(RuntimeError):
    """Raised when an external source fails licensing or AI-use policies."""
    pass

class LicenseChecker:
    PERMITTED_LICENSES = {
        "mit", "apache-2.0", "bsd-2-clause", "bsd-3-clause", "isc",
        "cc0-1.0", "cc-by-4.0", "cc-by-sa-4.0", "cc-by-sa-3.0",
        "arxiv-nonexclusive", "public-domain", "open-access"
    }

    @classmethod
    def validate(cls, item: IngestionItem) -> None:
        if "reddit.com" in item.source_domain.lower() or item.source_name.lower() == "reddit":
            if not item.evidence_only:
                raise LicensePolicyError(
                    "Reddit content cannot be ingested as direct knowledge. It is restricted to evidence only."
                )
            if not item.metadata.get("legal_review_approved", False):
                raise LicensePolicyError(
                    "Reddit ingestion is blocked pending legal review approval (flag 'legal_review_approved' missing)."
                )

            if not item.ai_use_allowed:
                raise LicensePolicyError(
                    "Reddit content cannot be used for AI training or knowledge ingestion."
                )

            if not item.scraping_allowed:
                raise LicensePolicyError(
                    "Reddit content cannot be scraped for ingestion."
                )

            normalized_license = (item.license_name or "").strip().lower()
            if normalized_license and normalized_license not in cls.PERMITTED_LICENSES:
                if not item.metadata.get("manual_license_override", False):
                    raise LicensePolicyError(
                        f"License '{item.license_name}' is not in approved list. Provide 'manual_license_override' to proceed."
                    )