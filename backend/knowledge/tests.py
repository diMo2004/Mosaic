from django.test import TestCase
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
# Create your tests here.

from knowledge.models import (
    CanonicalClaim,
    Concept,
    ConceptRelationship,
    Evidence,
    ExtractedClaim,
    Source,
    SourceDocument,
    UnmappedConceptReview,
)

class KnowledgeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author")
        self.source = Source.objects.create(
            name="Official Python Docs",
            source_type=Source.SOURCE_TYPE_OFFICIAL,
            authority_score=Decimal("0.95"),
        )
        self.concept_python = Concept.objects.create(name="Python", slug="python")
        self.concept_django = Concept.objects.create(name="Django", slug="django")

    def test_concept_relationship_creation(self):
        rel = ConceptRelationship.objects.create(
            from_concept=self.concept_django,
            to_concept=self.concept_python,
            relation_type=ConceptRelationship.RELATION_BUILDS_ON,
        )
        self.assertEqual(str(rel), "Django --(builds_on)--> Python")

    def test_canonical_claim_and_evidence(self):
        doc = SourceDocument.objects.create(
            source=self.source,
            title="Django Overview",
            document_type=SourceDocument.DOCUMENT_TYPE_DOC,
            raw_text="Django is a high-level Python web framework.",
        )
        claim = ExtractedClaim.objects.create(
            source_document=doc,
            text="Django is a Python web framework.",
        )
        evidence = Evidence.objects.create(
            claim=claim,
            source=self.source,
            relation=Evidence.SUPPORTS,
            relevance_score=Decimal("0.90"),
        )
        self.assertEqual(claim.evidence_items.count(), 1)
        self.assertEqual(evidence.relation, Evidence.SUPPORTS)

    def test_unmapped_concept_review_creation(self):
        review = UnmappedConceptReview.objects.create(
            suggested_name="PyTorch Lightning",
            context_text="PyTorch Lightning is used for training models.",
        )
        self.assertEqual(review.status, UnmappedConceptReview.STATUS_PENDING)

class KnowledgeAPIPermissionTests(APITestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(username="student", password="pw")
        self.admin_user = User.objects.create_superuser(username="admin", password="pw")
        self.source = Source.objects.create(name="Test Source", source_type=Source.SOURCE_TYPE_COMMUNITY)

    def test_unauthenticated_cannot_access_sources(self):
        response = self.client.get("/api/knowledge/sources/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_can_read_sources_but_not_create(self):
        self.client.force_authenticate(user=self.regular_user)
        get_res = self.client.get("/api/knowledge/sources/")
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)

        post_res = self.client.post("/api/knowledge/sources/", {"name": "New Source"}, format="json")
        self.assertEqual(post_res.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_user_can_create_source(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            "/api/knowledge/sources/",
            {"name": "Admin Added Source", "source_type": Source.SOURCE_TYPE_OFFICIAL},
             format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
