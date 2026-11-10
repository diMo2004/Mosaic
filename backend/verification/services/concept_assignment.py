import os
import json
import re
import networkx as nx
from django.conf import settings
from google import genai
from knowledge.models import Concept, ConceptRelationship, UnmappedConceptReview
import logging
import pickle
from django.core.cache import cache

logger = logging.getLogger(__name__)

GRAPH_CACHE_KEY = "MOSAIC_NX_GRAPH_BYTES"
GRAPH_CACHE_TTL_SECONDS = 3600
ROOT_CONCEPT_NAME = "Computer Science & Engineering"


def build_concept_graph():
    """Build the taxonomy graph from Concept and ConceptRelationship rows."""
    G = nx.DiGraph()
    for concept_id, name in Concept.objects.values_list("id", "name"):
        G.add_node(concept_id, name=name)
    for from_id, to_id, relation in ConceptRelationship.objects.values_list(
        "from_concept_id", "to_concept_id", "relation_type",
    ):
        G.add_edge(from_id, to_id, relation=relation)
    return G


def get_cached_nx_graph():
    cached_bytes = cache.get(GRAPH_CACHE_KEY)
    if cached_bytes:
        return pickle.loads(cached_bytes)

    G = build_concept_graph()
    # Never cache an empty graph: it would hide a later taxonomy seed for the TTL.
    if G.number_of_nodes():
        cache.set(GRAPH_CACHE_KEY, pickle.dumps(G), timeout=GRAPH_CACHE_TTL_SECONDS)
    return G

def invalidate_cached_graph():
    cache.delete(GRAPH_CACHE_KEY)

class ConceptAssignmentService:
    def __init__(self):
        self.graph = get_cached_nx_graph()
        api_key = getattr(settings, "GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
        self.client = genai.Client(api_key=api_key) if api_key else None
        self.model_name = getattr(settings, "GEMINI_CLAIM_MODEL", "gemini-3.8-flash")

    def _find_anchor_nodes(self, text: str, max_anchors: int = 3):
        """Finds direct keyword matches in text against concept names, longest names first."""
        text_lower = text.lower()
        matched_nodes_ids = []

        nodes = sorted(
            self.graph.nodes(data=True),
            key=lambda node: len(node[1].get("name", "")),
            reverse=True,
        )
        for node_id, data in nodes:
            concept_name = data.get("name", "").lower()
            if concept_name == ROOT_CONCEPT_NAME.lower():
                continue
            if len(concept_name) >= 3 and re.search(r'\b' + re.escape(concept_name) + r'\b', text_lower):
                matched_nodes_ids.append(node_id)
                if len(matched_nodes_ids) >= max_anchors:
                    break

        return matched_nodes_ids

    def retrieve_subgraph_candidates(self, text: str, hint_concept_id=None):
        """
        Retrieves a focused 1-hop sub-graph around anchor nodes.
        Returns an ordered list of candidate dictionaries: [{'id': int, 'name': str}],
        best lexical matches (and the discovery topic hint) first.
        """
        anchors = self._find_anchor_nodes(text)
        if hint_concept_id in self.graph and hint_concept_id not in anchors:
            anchors.append(hint_concept_id)
        if not anchors:
            roots = [n for n, d in self.graph.nodes(data=True) if self.graph.in_degree(n) == 0][:10]
            return [{"id": n, "name": self.graph.nodes[n]["name"]} for n in roots]

        ordered = list(anchors)
        for anchor in anchors:
            for neighbour in sorted(set(self.graph.predecessors(anchor)) | set(self.graph.successors(anchor))):
                if neighbour not in ordered:
                    ordered.append(neighbour)

        return [{"id": cid, "name": self.graph.nodes[cid]["name"], "anchor": cid in anchors} for cid in ordered if cid in self.graph]

    def _root_concept(self):
        return Concept.objects.get_or_create(
            name=ROOT_CONCEPT_NAME,
            defaults={"slug": "cse"}
        )[0]

    def assign_concept(self, claim_text: str, source_claim=None, hint_concept_id=None):
        """
        Assigns an official Concept from the sub-graph. If the text contains an unmapped technology outside the taxonomy,
        creates an UnmappedConceptReview item for developers.
        """

        candidates = self.retrieve_subgraph_candidates(claim_text, hint_concept_id=hint_concept_id)
        candidate_ids = {candidate["id"] for candidate in candidates}

        prompt = f"""
You are a Computer Science Knowledge Taxonomy classifier.
Analyze the claim below and select the single most accurate Concept from the given candidates.

Claim: "{claim_text}"
Allowed Candidate Concepts:
{json.dumps([{"id": c["id"], "name": c["name"]} for c in candidates], indent=2)}

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
        if self.client is not None and candidates:
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config={"response_mime_type": "application/json"}
                )
                result = json.loads(response.text)
                concept_id = result.get("concept_id")
                unmapped_name = result.get("unmapped_concept_name")

                # Only accept IDs that were offered; ignore hallucinated IDs.
                if concept_id in candidate_ids:
                    concept = Concept.objects.filter(id=concept_id).first()
                    if concept:
                        return concept

                if unmapped_name and str(unmapped_name).strip():
                    clean_name = str(unmapped_name).strip()[:255]
                    UnmappedConceptReview.objects.create(
                        suggested_name=clean_name,
                        context_claim=source_claim,
                        context_text=claim_text,
                    )

            except Exception as e:
                logger.warning("ConceptAssignmentService LLM concept assignment failed: %s", e)

        # Deterministic fallback: the best lexical anchor, else the root umbrella
        # concept. Never an arbitrary unrelated root.
        anchor_ids = [candidate["id"] for candidate in candidates if candidate.get("anchor")]
        if anchor_ids:
            concept = Concept.objects.filter(id=anchor_ids[0]).first()
            if concept:
                return concept

        return self._root_concept()
