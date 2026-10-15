import React from 'react';
import type { FlashcardDTO, CardViewState } from '@/types/flashcard';
import { CardShell } from './CardShell';
import { ConceptVisualCard } from './ConceptVisualCard';
import { RecallCard } from './RecallCard';
import { QuickQuizCard } from './QuickQuizCard';
interface CardRendererProps {
    card: FlashcardDTO;
    viewState: CardViewState;
    onRevealAnswer?: (cardId: number) => void;
    onSelectOption?: (cardId: number, optionIndex: number) => void;
    onToggleSave?: (cardId: number) => void;
    onMarkUnderstood?: (cardId: number) => void;
    onOpenExplain?: (claimId: number) => void;
    onOpenDetail?: (cardId: number) => void;
    cardHeight?: number;
}
export const CardRenderer: React.FC<CardRendererProps> = ({
    card,
    viewState,
    onRevealAnswer,
    onSelectOption,
    onToggleSave,
    onMarkUnderstood,
    onOpenExplain,
    onOpenDetail,
    cardHeight,
}) => {
    // Render matching template based on card_type
    const renderTemplate = () => {
        switch (card.card_type) {
            case 'concept_visual':
                return <ConceptVisualCard card={card} />;
            case 'quick_quiz':
                // Graceful fallback to recall if quiz options are empty
                if (!card.quiz_options || card.quiz_options.length === 0) {
                    return (
                        <RecallCard
                            card={card}
                            viewState={viewState}
                            onReveal={() => onRevealAnswer?.(card.id)}
                        />
                    );
                }
                return (
                    <QuickQuizCard
                        card={card}
                        viewState={viewState}
                        onSelectOption={(idx) => onSelectOption?.(card.id, idx)}
                    />
                );
            case 'recall':
            default:
                return (
                    <RecallCard
                        card={card}
                        viewState={viewState}
                        onReveal={() => onRevealAnswer?.(card.id)}
                    />
                );
        }
    };
    return (
        <CardShell
            card={card}
            isUnderstood={viewState?.understood}
            isSaved={viewState?.saved}
            onToggleUnderstood={() => onMarkUnderstood?.(card.id)}
            onToggleSave={() => onToggleSave?.(card.id)}
            onOpenExplain={
                card.canonical_claim_id && onOpenExplain
                    ? () => onOpenExplain(card.canonical_claim_id!)
                    : undefined
            }
            onOpenDetail={
                onOpenDetail ? () => onOpenDetail(card.id) : undefined
            }
            cardHeight={cardHeight}
        >
            {renderTemplate()}
        </CardShell>
    );
};