import os
import json
import re
import networkx as nx
from django.conf import settings
from google import genai
from knowledge.models import Concept, ConceptRelationship, UnmappedConceptReview

_CACHED_GRAPH = None

def get_cached_nx_graph():
    """Builds and caches the NetworkX in-memory graph from PostgreSQL."""
    global _CACHED_GRAPH
    if _CACHED_GRAPH is None:
        graph = nx.DiGraph()
        for concept in Concept.objects.all():
            graph.add_node(concept.id, name=concept.name, slug=concept.slug)

        for relationship in ConceptRelationship.objects.all():
            graph.add_edge(relationship.from_concept.id, relationship.to_concept.id, type=relationship.relation_type)

        _CACHED_GRAPH = graph
    return _CACHED_GRAPH

def invalidate_cached_graph():
    global _CACHED_GRAPH
    _CACHED_GRAPH = None

class ConceptAssignmentService:
    def __init__(self):
        self.graph = get_cached_nx_graph()
        api_key = getattr(settings, "GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
        self.client = genai.Client(api_key=api_key)
        self.model_name = getattr(settings, "GEMINI_CLAIM_MODEL", "gemini-3.6-flash")

    def _find_anchor_nodes(self, text: str, max_anchors: int = 3):
        """Finds direct keywor matches in text against concept names."""
        text_lower = text.lower()
        matched_nodes_ids = []

        for node_id, data in self.graph.nodes(data=True):
            concept_name = data.get("name", "").lower()
            if len(concept_name) >= 3 and re.search(r'\b' + re.escape(concept_name) + r'\b', text_lower):
                matched_nodes_ids.append(node_id)
                if len(matched_nodes_ids) >= max_anchors:
                    break

        return matched_nodes_ids

    def retrieve_subgraph_candidates(self, text: str):
        """
        Retrieves a focused 1-hop sub-graph around anchor nodes.
        Returns a list of candidate dictionaries: [{'id': int, 'name': str}]
        """
        anchors = self._find_anchor_nodes(text)
        if not anchors:
            roots = [n for n, d in self.graph.nodes(data=True) if self.graph.in_degree(n) == 0][:10]
            return [{"id": n, "name": self.graph.nodes[n]["name"]} for n in roots]

        candidate_ids = set(anchors)
        for anchor in anchors:
            candidate_ids.update(self.graph.predecessors(anchor))
            candidate_ids.update(self.graph.successors(anchor))

        return [{"id": cid, "name": self.graph.nodes[cid]["name"]} for cid in candidate_ids if cid in self.graph]

    def assign_concept(self, claim_text: str, source_claim=None):
        """
        Assigns an official Concept from the sub-graph. If the text contains an unmapped technology outside the taxonomy,
        creates an UnmappedConceptReview item for developers.
        """

        candidates = self.retrieve_subgraph_candidates(claim_text)

        prompt = f"""
You are a Computer Science Knowledge Taxonomy classifier.
Analyze the claim below and select the single most accurate Concept from the given candidates.

Claim: "{claim_text}"
Allowed Candidate Concepts:
{json.dumps(candidates, indent=2)}

Rules:
1. If one of the candidate concepts accurately classifies this claim, return its integer "concept_id".
2. If the claim is about a specific technology, framework, or algorithm NOT present in the candidate list,
   set "concept_id" to null and provide the technology name in "unmapped_concept_name".
3. Provide a short reason.
Output strictly valid JSON in this schema:
{{
  "concept_id": 12 or null,
  "unmapped_concept_name": "Name of novel concept if outside candidates" or null,
  "reason": "Brief rationale"
}}
"""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            result = json.loads(response.text)
            concept_id = result.get("concept_id")
            unmapped_name = result.get("unmapped_concept_name")

            if concept_id and Concept.objects.filter(id=concept_id).exists():
                return Concept.objects.get(id=concept_id)

            if unmapped_name and unmapped_name.strip():
                clean_name = unmapped_name.strip()
                UnmappedConceptReview.objects.create(
                    suggested_name=clean_name,
                    context_claim=source_claim,
                    context_text=claim_text,
                )

        except Exception as e:
            print(f"[ConceptAssignmentService Warning] LLM concept assignment failed: {e}.")

        if candidates:
            return Concept.objects.get(id=candidates[0]["id"])

        return Concept.objects.get_or_create(
            name="Computer Science & Engineering",
            defaults={"slug": "cse"}
        )[0]