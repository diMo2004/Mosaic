import os
import re
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.conf import settings
from knowledge.models import Concept, ConceptRelationship

class Command(BaseCommand):
    help = "Seeds the CSE technology knowledge graph from docs/cse_tech_concepts.md"

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR.parent
        doc_path = os.path.join(base_dir, "docs", "cse_tech_concepts.md")

        if not os.path.exists(doc_path):
            self.stderr.write(f"Could not find concepts file at {doc_path}")
            return

        self.stdout.write(f"Reading CSE concepts from {doc_path}")
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        node_def_pattern = re.compile(r'([A-Za-z0-9_]+)\[([^\]]+)\]')
        edge_pattern = re.compile(r'([A-Za-z0-9_]+)\s*-->\s*([A-Za-z0-9_]+)')

        node_map = {}
        for match in node_def_pattern.finditer(content):
            node_id, display_name = match.groups()
            node_map[node_id] = display_name.strip()

        Concept.objects.get_or_create(
            name="Computer Science & Engineering",
            defaults={"slug": "cse", "description": "Root umbrella taxonomy node."}
        )
        created_count = 0
        concept_objects = {}

        for node_id, display_name in node_map.items():
            slug = slugify(display_name) or slugify(node_id)
            concept, created = Concept.objects.get_or_create(
                slug=slug,
                defaults={"name": display_name, "description": f"Concept node for {display_name}."}
            )
            concept_objects[node_id] = concept
            if created:
                created_count += 1

        self.stdout.write(f"Created {created_count} new concepts. Total mapped: {len(concept_objects)}")

        edges_created = 0
        for match in edge_pattern.finditer(content):
            from_id, to_id = match.groups()
            from_concept = concept_objects.get(from_id)
            to_concept = concept_objects.get(to_id)

            if from_concept and to_concept and from_concept != to_concept:
                _, created = ConceptRelationship.objects.get_or_create(
                    from_concept=from_concept,
                    to_concept=to_concept,
                    relation_type=ConceptRelationship.RELATION_PARENT,
                )
                if created:
                    edges_created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded CSE concepts and relationships. Created {created_count} concepts and {edges_created} relationships."
        ))

                            