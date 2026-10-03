import json
import math
from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from google import genai
from google.genai import types
from knowledge.models import Concept, ConceptRelationship
from learning.models import Flashcard, MasteryBadge, Questionnaire, QuestionnaireQuestion, UserProgress

class MasteryService:
    TIER_NAMES = {
        1: "Easy",
        2: "Moderate",
        3: "Intermediate",
        4: "Advanced",
        5: "Expert"
    }

    PASSING_THRESHOLDS = {
        1: 8,
        2: 8,
        3: 8,
        4: 5,
        5: 5,
    }

    TIER_REQUIREMENTS = {
        1: (0.20, 15),
        2: (0.35, 30),
        3: (0.50, 50),
        4: (0.65, 75),
        5: (0.80, 100),
    }

    def get_user_current_tier(self, user, concept: Concept) -> int:
        """Returns the next unpassed tier (1 to 5), or 6 if all 5 are passed."""
        passed_tiers = set(
            Questionnaire.objects.filter(
                user=user,
                concept=concept,
                status=Questionnaire.STATUS_PASSED,
            ).values_list("tier", flat=True)
        )
        for tier in range(1, 6):
            if tier not in passed_tiers:
                return tier
        return 6

    def check_eligibility_for_tier(self, user, concept: Concept, target_tier: int) -> dict:
        total_cards = Flashcard.objcts.filter(
            source_claim__concept=concept,
            is_active=True,
        ).count()

        if total_cards == 0:
            return {
                "eligible": False,
                "tier": target_tier,
                "reason": "No flashcards available for this concept.",
                "viewed_distinct": 0,
                "required_distict": 0,
            }

        highest_passed = Questionnaire.objects.filter(
            user=user,
            concept=concept,
            status=Questionnaire.STATUS_PASSED,
        ).aggregate(models.Max("tier"))["tier__max"] or 0

        if highest_passed >= target_tier:
            return {
                "eligible": True,
                "tier": target_tier,
                "reason": f"You have already passed tier {target_tier}.",
                "viewed_distinct": 0,
                "required_distict": 0,
            }

        if target_tier > highest_passed + 1:
            return {
                "eligible": False,
                "tier": target_tier,
                "reason": f"You must pass tier {highest_passed + 1} before attempting tier {target_tier}.",
                "viewed_distinct": 0,
                "required_distict": 0,
            }

        pct, cap = self.TIER_REQUIREMENTS.get(target_tier, (0.80, 100))
        required_distinct = min(cap, max(1, math.ceil(total_cards * pct)))

        viewed_distinct = UserProgress.objects.filter(
            user=user,
            flashcard__source_claim__concept=concept,
            view_count__gt=0,
        ).values("flashcard_id").distinct().count()

        is_eligible = viewed_distinct >= required_distinct
        cards_needed = max(0, required_distinct - viewed_distinct)

        return {
            "eligible": is_eligible,
            "tier": target_tier,
            "tier_name": self.TIER_NAMES[target_tier],
            "requird_percentage": int(pct * 100),
            "tier_cap": cap,
            "viewed_distinct": viewed_distinct,
            "required_distict": required_distinct,
            "cards_needed": cards_needed,
            "total_cards": total_cards,
            "reason": "" if is_eligible else f"Need {cards_needed} more distinct flashcard views ({viewed_distinct}/{required_distinct} for Tier {target_tier})."
        }

    def generate_questionnaire(self, user, concept: Concept) -> Questionnaire:
        current_tier = self.get_user_current_tier(user, concept)
        if current_tier > 5:
            raise ValueError("User has already passed all tiers for this concept.")
        eligibility = self.check_eligibility_for_tier(user, concept, current_tier)
        if not eligibility["eligibile"]:
            raise ValueError(eligibility["reason"])

        viewed_cards = list(
            Flashcard.objects.filter(
                source_claim__concept=concept,
                progress_items__user=user,
                progress_items__view_count__gt=0,
            ).distinct()[:50]
        )

        past_prompts = list(
            QuestionnaireQuestion.objects.filter(
                questionnaire__user=user,
                questionnaire__concept=concept,
            ).values_list("prompt", flat=True)
        )

        threshold = self.PASSING_THRESHOLDS[current_tier]
        questionnaire = Questionnaire.objects.create(
            user=user,
            concept=concept,
            tier=current_tier,
            passing_threshold=threshold,
        )

        questions_data = self._generate_mcqs_from_llm(
            concept=concept,
            viewed_cards=viewed_cards,
            tier=current_tier,
            exclude_prompts=past_prompts,
        )

        for q in questions_data:
            QuestionnaireQuestion.objects.create(
                questionnaire=questionnaire,
                prompt=q["prompt"],
                options=q["options"],
                correct_option_index=q["correct_index"],
                explanation=q.get("explanation", ""),
            )
        return questionnaire

    def _generate_mcqs_from_llm(self, concept, viewed_cards, tier, exclude_prompts):
        tier_guidelines = {
            1: "Easy: direct factual recall, definitions. Clear correct option.",
            2: "Moderate: basic comprehension and practical scenario application.",
            3: "Intermediate: reasoning, tracing behavior, or edge cases.",
            4: "Advanced: subtle nuances, plausible distractors, minimal giveaway words.",
            5: "Expert: deep technical subtlety, highly deceptive distractors, ZERO scope for process-of-elimination guessing.",
        }
        cards_summary = "\n".join(
            [f"- Q: {c.prompt} | A: {c.answer}" for c in viewed_cards[:30]]
        )
        prompt_text = f"""
You are an expert examiner in Computer Science for concept: '{concept.name}'.
Generate exactly 10 distinct Multiple Choice Questions (MCQs) for difficulty level: {self.TIER_NAMES[tier]}.
Guideline: {tier_guidelines[tier]}
Ground the questions on these studied flashcards:
{cards_summary}
Do not repeat any of these previously asked question prompts:
{json.dumps(exclude_prompts[:50])}
Return STRICT JSON format as a list of 10 objects:
[
  {{
    "prompt": "Question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_index": 0,
    "explanation": "Why this is correct"
  }}
]
"""
        api_key = getattr(settings, "GEMINI_API_KEY", "")
        if not api_key:
            return [
                {
                    "prompt": f"Practice question {i+1} on {concept.name} (Tier {tier})?",
                    "options": ["Correct Answer", "Distractor 1", "Distractor 2", "Distractor 3"],
                    "correct_index": 0,
                    "explanation": "Placeholder grounding explanation.",
                }
                for i in range(10)
            ]
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=getattr(settings, "GEMINI_CLAIM_MODEL", "gemini-2.5-flash"),
            contents=prompt_text,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        data = json.loads(response.text)
        return data[:10]
    @transaction.atomic
    def grade_questionnaire(self, questionnaire: Questionnaire, answers: list[dict]) -> dict:
        questions = {q.id: q for q in questionnaire.questions.all()}
        correct_count = 0
        for ans in answers:
            qid = ans.get("question_id")
            selected = ans.get("selected_index")
            if qid in questions:
                q = questions[qid]
                q.user_selected_index = selected
                q.is_correct = (selected == q.correct_option_index)
                if q.is_correct:
                    correct_count += 1
                q.save(update_fields=["user_selected_index", "is_correct"])
        passed = correct_count >= questionnaire.passing_threshold
        questionnaire.score = correct_count
        questionnaire.status = Questionnaire.STATUS_PASSED if passed else Questionnaire.STATUS_FAILED
        questionnaire.completed_at = timezone.now()
        questionnaire.save(update_fields=["score", "status", "completed_at"])
        badge_awarded = None
        superset_badge = None
        if passed and questionnaire.tier == 5:
            badge_awarded, superset_badge = self._award_badges_if_complete(
                user=questionnaire.user,
                concept=questionnaire.concept,
            )
        return {
            "score": correct_count,
            "total": len(questions),
            "passed": passed,
            "threshold": questionnaire.passing_threshold,
            "status": questionnaire.status,
            "badge_awarded": badge_awarded is not None,
            "superset_badge_awarded": superset_badge is not None,
        }
    def _award_badges_if_complete(self, user, concept: Concept):
        passed_attempts = Questionnaire.objects.filter(
            user=user,
            concept=concept,
            status=Questionnaire.STATUS_PASSED,
        ).order_by("tier")
        progression_data = {
            f"tier_{q.tier}": {
                "score": q.score,
                "passed_at": q.completed_at.isoformat() if q.completed_at else None,
            }
            for q in passed_attempts
        }
        # Concept Mastery Badge
        badge, _ = MasteryBadge.objects.get_or_create(
            user=user,
            concept=concept,
            defaults={
                "is_superset": False,
                "difficulty_progression": progression_data,
            },
        )
        # Superset Check (via ConceptRelationship)
        parent_relations = ConceptRelationship.objects.filter(
            from_concept=concept,
            relation_type=ConceptRelationship.RELATION_PARENT,
        ).select_related("to_concept")
        superset_badge = None
        for rel in parent_relations:
            parent_concept = rel.to_concept
            child_ids = list(
                ConceptRelationship.objects.filter(
                    to_concept=parent_concept,
                    relation_type=ConceptRelationship.RELATION_PARENT,
                ).values_list("from_concept_id", flat=True)
            )
            total_subtopics = len(child_ids)
            # Rule: 10 subtopics, or ALL if fewer than 10
            required_subtopics_count = min(10, total_subtopics) if total_subtopics > 0 else 0
            earned_child_badges = MasteryBadge.objects.filter(
                user=user,
                concept_id__in=child_ids,
                is_superset=False,
            ).count()
            if earned_child_badges >= required_subtopics_count and required_subtopics_count > 0:
                superset_badge, _ = MasteryBadge.objects.get_or_create(
                    user=user,
                    concept=parent_concept,
                    defaults={
                        "is_superset": True,
                        "difficulty_progression": {
                            "completed_subtopics_count": earned_child_badges,
                            "required_count": required_subtopics_count,
                            "awarded_at": timezone.now().isoformat(),
                        },
                    },
                )
        return badge, superset_badge