import { useState, useEffect, useCallback, useRef } from 'react';
import {
    getFlashcards,
    markFlashcardUnderstood,
    recordFlashcardView,
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
    loadMore: () => void;
    isLoadingMore: boolean;
    sessionExhausted: boolean;
    sessionComplete: boolean;
}

function normaliseResponse(res: FlashcardListResponse): FlashcardDTO[] {
    return Array.isArray(res) ? res : res.results ?? [];
}

export function useFlashcardFeed(): UseFeedReturn {
    const [cards, setCards] = useState<FlashcardDTO[]>([]);
    const [status, setStatus] = useState<FeedStatus>('idle');
    const [isLoadingMore, setIsLoadingMore] = useState(false);
    const [sessionExhausted, setSessionExhausted] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [viewStates, setViewStates] = useState<Record<number, CardViewState>>({});
    const [seenCardIds, setSeenCardIds] = useState<Set<number>>(new Set());
    const seenCardIdsRef = useRef(seenCardIds);
    const recordedCardIds = useRef(new Set<number>());
    const sessionIdRef = useRef<string | undefined>(undefined);

    const createSessionId = () => 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, char => {
        const value = Math.floor(Math.random() * 16);
        return (char === 'x' ? value : (value & 0x3) | 0x8).toString(16);
    });

    const load = useCallback(async (isRefresh = false) => {
        setStatus(isRefresh ? 'refreshing' : 'loading');
        setError(null);
        try {
            if (!sessionIdRef.current || isRefresh) {
                sessionIdRef.current = createSessionId();
                setSessionExhausted(false);
            }
            const response = await getFlashcards(sessionIdRef.current);
            const nextCards = normaliseResponse(response);
            if (!Array.isArray(response) && response.session_id) {
                sessionIdRef.current = response.session_id;
            }
            if (!Array.isArray(response) && typeof response.session_exhausted === 'boolean') {
                setSessionExhausted(response.session_exhausted);
            }
            setCards(nextCards);
            setViewStates(previous => {
                const next: Record<number, CardViewState> = {};
                for (const card of nextCards) {
                    next[card.id] = previous[card.id] ?? initialCardViewState(card);
                }
                return next;
            });
            setStatus('success');
            if (isRefresh) {
                seenCardIdsRef.current = new Set();
                recordedCardIds.current.clear();
                setSeenCardIds(seenCardIdsRef.current);
                setCurrentIndex(0);
            }
        } catch (err: unknown) {
            const apiMessage = (err as {
                response?: { data?: { detail?: string } };
                message?: string;
            })?.response?.data?.detail;
            const message = apiMessage ?? (err as { message?: string })?.message;
            setError(message ?? 'Failed to load feed');
            setStatus('error');
        }
    }, []);

    const loadMore = useCallback(async () => {
        if (isLoadingMore || sessionExhausted || status === 'loading' || status === 'refreshing') {
            return;
        }
        setIsLoadingMore(true);
        try {
            const response = await getFlashcards(sessionIdRef.current);
            const additionalCards = normaliseResponse(response);
            if (!Array.isArray(response) && typeof response.session_exhausted === 'boolean') {
                setSessionExhausted(response.session_exhausted);
            }
            if (additionalCards.length > 0) {
                setCards(prev => {
                    const existingIds = new Set(prev.map(c => c.id));
                    const newItems = additionalCards.filter(c => !existingIds.has(c.id));
                    return [...prev, ...newItems];
                });
                setViewStates(previous => {
                    const next = { ...previous };
                    for (const card of additionalCards) {
                        if (!next[card.id]) {
                            next[card.id] = initialCardViewState(card);
                        }
                    }
                    return next;
                });
            }
        } catch {
            // Silently swallow pagination errors to not disturb active swiping
        } finally {
            setIsLoadingMore(false);
        }
    }, [isLoadingMore, sessionExhausted, status]);

    useEffect(() => {
        void load();
    }, [load]);

    const onCardVisible = useCallback((index: number) => {
        const card = cards[index];
        if (!card) return;

        setCurrentIndex(current => current === index ? current : index);
        if (!seenCardIdsRef.current.has(card.id)) {
            const nextSeen = new Set(seenCardIdsRef.current);
            nextSeen.add(card.id);
            seenCardIdsRef.current = nextSeen;
            setSeenCardIds(nextSeen);
        }
        if (!recordedCardIds.current.has(card.id)) {
            recordedCardIds.current.add(card.id);
            void recordFlashcardView(card.id, sessionIdRef.current).catch(() => {
                // A transient analytics failure must not interrupt the study session.
            });
        }

        // Prefetch next batch when user gets within 3 cards of the bottom
        if (index >= cards.length - 3 && !sessionExhausted && !isLoadingMore) {
            void loadMore();
        }
    }, [cards, sessionExhausted, isLoadingMore, loadMore]);

    const patchViewState = useCallback(
        (cardId: number, patch: Partial<CardViewState>) => {
            setViewStates(previous => ({
                ...previous,
                [cardId]: { ...previous[cardId], ...patch },
            }));
        },
        [],
    );

    const revealAnswer = useCallback(
        (cardId: number) => patchViewState(cardId, { revealed: true, answered: true }),
        [patchViewState],
    );

    const selectOption = useCallback((cardId: number, optionIndex: number) => {
        setViewStates(previous => {
            if (previous[cardId]?.answered) return previous;
            return {
                ...previous,
                [cardId]: {
                    ...previous[cardId],
                    selectedOption: optionIndex,
                    answered: true,
                },
            };
        });
    }, []);

    const toggleSave = useCallback(async (cardId: number) => {
        const current = viewStates[cardId];
        if (!current) return;
        const wasSaved = current.saved;
        patchViewState(cardId, { saved: !wasSaved });
        try {
            if (wasSaved) await unsaveFlashcard(cardId);
            else await saveFlashcard(cardId);
        } catch {
            patchViewState(cardId, { saved: wasSaved });
        }
    }, [viewStates, patchViewState]);

    const markUnderstood = useCallback(async (cardId: number) => {
        const wasUnderstood = viewStates[cardId]?.understood ?? false;
        patchViewState(cardId, { understood: true });
        try {
            await markFlashcardUnderstood(cardId, true);
        } catch {
            patchViewState(cardId, { understood: wasUnderstood });
        }
    }, [patchViewState, viewStates]);

    const refresh = useCallback(() => { void load(true); }, [load]);
    const sessionComplete = sessionExhausted && cards.length > 0 && cards.every(card => seenCardIds.has(card.id));

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
        loadMore,
        isLoadingMore,
        sessionExhausted,
        sessionComplete,
    };
}
