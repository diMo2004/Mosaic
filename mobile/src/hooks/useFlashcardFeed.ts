import { useState, useEffect, useCallback, useRef } from 'react';
import {
    getFlashcards,
    markFlashcardUnderstood,
    saveFlashcard,
    unsaveFlashcard,
} from '@/api/learning';
import {
    FlashcardDTO,
    FlashcardListResponse,
    CardViewState,
    initialCardViewState,
} from '@/types/flashcard';

export type FeedStatus = 'idle' | 'loading' | 'refreshing' | 'success' | 'error';

export interface UseFeedReturn {
    cards: FlashcardDTO[];
    status: FeedStatus;
    error: string | null;
    currentIndex: number;
    viewStates: Record<number, CardViewState>;
    onCardVisible: (index: number) => void;
    revealAnswer: (cardId: number) => void;
    selectOption: (cardId: number, optionIndex: number) => void;
    toggleSave: (cardId: number) => Promise<void>;
    markUnderstood: (cardId: number) => Promise<void>;
    refresh: () => void;
    sessionComplete: boolean;
}

function normaliseResponse(res: FlashcardListResponse): FlashcardDTO[] {
    if (Array.isArray(res)) return res;
    return res.results ?? [];
}

export function useFlashcardFeed(): UseFeedReturn {
    const [cards, setCards] = useState<FlashcardDTO[]>([]);
    const [status, setStatus] = useState<FeedStatus>('idle');
    const [error, setError] = useState<string | null>(null);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [viewStates, setViewStates] = useState<Record<number, CardViewState>>({});
    const seenIndices = useRef<Set<number>>(new Set());
    const load = useCallback(async (isRefresh = false) => {
        setStatus(isRefresh ? 'refreshing' : 'loading');
        setError(null);
        try {
            const res: FlashcardListResponse = await getFlashcards();
            const list = normaliseResponse(res);
            setCards(list);
            setViewStates(prev => {
                const next = { ...prev };
                for (const card of list) {
                    if (!(card.id in next)) {
                        next[card.id] = initialCardViewState(card);
                    }
                }
                return next;
            });
            setStatus('success');
            if (isRefresh) {
                seenIndices.current = new Set();
                setCurrentIndex(0);
            } 
        } catch (err: unknown) {
                const msg = 
                    (err as { response?: { data?: { detail?: string}}; message?: string})
                        ?.response?.data?.detail??
                    (err as { message?: string})?.message ??
                    'Failed to load feed';
                setError(msg);
                setStatus('error');
            }
        }, []);
        useEffect(() => {
            load(false);
        }, [load]);
        const onCardVisible = useCallback((index: number) => {
            setCurrentIndex(current => current === index ? current : index);
            seenIndices.current.add(index);
    }, []);
    const patchViewState = useCallback(
        (cardId: number, patch: Partial<CardViewState>) => {
            setViewStates(prev => ({
                ...prev,
                [cardId]: { ...prev[cardId], ...patch},
            }));
        },
        [],
    );
    const revealAnswer = useCallback(
        (cardId: number) => patchViewState(cardId, { revealed: true, answered: true}),
        [patchViewState],
    );
    const selectOption = useCallback(
        (cardId: number, optionIndex: number) => {
            setViewStates(prev => {
                if (prev[cardId]?.answered) return prev;
                return {
                    ...prev,
                    [cardId]: { ...prev[cardId], selectedOption: optionIndex, answered: true },
                };
            });
        },
        [],
    );
    const toggleSave = useCallback(
        async (cardId: number) => {
            const current = viewStates[cardId];
            if (!current) return;
            const wasSaved = current.saved;
            patchViewState(cardId, { saved: !wasSaved });
            try {
                if (wasSaved) {
                    await unsaveFlashcard(cardId);
                } else {
                    await saveFlashcard(cardId);
                }
            } catch {
                patchViewState(cardId, { saved: wasSaved });
            }
        },
        [viewStates, patchViewState],
    );
    const markUnderstood = useCallback(
        async (cardId: number) => {
            patchViewState(cardId, { understood: true });
            try {
                await markFlashcardUnderstood(cardId, true);
            } catch {
                patchViewState(cardId, { understood: false});
            }
        },
        [patchViewState],
    );
    const sessionComplete = cards.length > 0 && seenIndices.current.size >= cards.length;
    const refresh = useCallback(() => load(true), [load]);
    return {
        cards,
        status,
        error,
        currentIndex,
        viewStates,
        onCardVisible,
        revealAnswer,
        selectOption,
        toggleSave,
        markUnderstood,
        refresh,
        sessionComplete,
    };
};