export type CardType = 'concept_visual' | 'recall' | 'quick_quiz';
export type Difficulty = 'beginner' | 'intermediate' | 'advanced';
export type FeedbackType = 'like' | 'dislike' | 'confusing' | 'incorrect' | 'too_easy' | 'too_hard';

export interface EvidenceItem {
    source: string;
    title: string;
    url: string | null;
    excerpt: string | null;
    relation : string;
    relevance_score: string;
}

export interface QuizOption {
    text: string;
    is_correct: boolean;
    explanation: string;
}

export interface FlashcardDTO {
    id: number;
    title: string;
    prompt: string;
    answer: string;
    explanation: string;
    difficulty: Difficulty;
    card_type: CardType;
    quiz_options: QuizOption[] | null;
    key_points: string[] | null;
    visual_hint: string | null;
    source_claim: number | null;
    canonical_claim_id: number | null;
    canonical_claim_text: string | null;
    concept_id: number | null;
    concept_name: string | null;
    evidence: EvidenceItem[];
    created_at: string;
    updated_at: string;
    is_saved: boolean;
    playlist_ids: number[];
}

export type FlashcardListResponse = 
    | FlashcardDTO[] 
    | { results: FlashcardDTO[]; count: number; next: string | null; previous: string | null };
    
export interface CardViewState {
    revealed: boolean;
    selectedOption: number | null;
    answered: boolean;
    saved: boolean;
    understood: boolean;
}

export function initialCardViewState(card: FlashcardDTO): CardViewState {
    return {
        revealed: false,
        selectedOption: null,
        answered: false,
        saved: card.is_saved,
        understood: false,
    };
}