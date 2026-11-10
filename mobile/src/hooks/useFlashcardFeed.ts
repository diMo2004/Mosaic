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
    /** Ask the server for cards generated since the session ran out, keeping position. */
    checkForNewCards: () => void;
    isLoadingMore: boolean;
    sessionExhausted: boolean;
    sessionComplete: boolean;
    paginationError: string | null;
}

const DEFAULT_RECHECK_SECONDS = 120;

function normaliseResponse(res: FlashcardListResponse): FlashcardDTO[] {
    return Array.isArray(res) ? res : res.results ?? [];
}

function errorMessage(err: unknown, fallback: string): string {
    const apiMessage = (err as {
        response?: { data?: { detail?: string } };
        message?: string;
    })?.response?.data?.detail;
    return apiMessage ?? (err as { message?: string })?.message ?? fallback;
}

/**
 * @param active  whether the feed screen is focused and the app foregrounded;
 *                exhausted-session rechecks only run while active.
 */
export function useFlashcardFeed(active = true): UseFeedReturn {
    const [cards, setCards] = useState<FlashcardDTO[]>([]);
    const [status, setStatus] = useState<FeedStatus>('idle');
    const [isLoadingMore, setIsLoadingMore] = useState(false);
    const [sessionExhausted, setSessionExhausted] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [paginationError, setPaginationError] = useState<string | null>(null);
    const [recheckSeconds, setRecheckSeconds] = useState(DEFAULT_RECHECK_SECONDS);
    const loadingMoreRef = useRef(false);
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
            if (!Array.isArray(response) && response.retry_after_seconds) {
                setRecheckSeconds(response.retry_after_seconds);
            }
            setPaginationError(null);
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
            setError(errorMessage(err, 'Failed to load feed'));
            setStatus('error');
        }
    }, []);

    // Fetch the next page of the same server session. `force` also asks after the
    // session was exhausted, which returns cards persisted since then (the server
    // excludes everything already served in this session, so nothing repeats).
    const fetchMore = useCallback(async (force: boolean) => {
        if (loadingMoreRef.current || (!force && sessionExhausted) || status === 'loading' || status === 'refreshing') {
            return;
        }
        if (!sessionIdRef.current) return;
        loadingMoreRef.current = true;
        setIsLoadingMore(true);
        try {
            const response = await getFlashcards(sessionIdRef.current);
            const additionalCards = normaliseResponse(response);
            if (!Array.isArray(response) && typeof response.session_exhausted === 'boolean') {
                setSessionExhausted(response.session_exhausted);
            }
            if (!Array.isArray(response) && response.retry_after_seconds) {
                setRecheckSeconds(response.retry_after_seconds);
            }
            setPaginationError(null);
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
        } catch (err: unknown) {
            // Keep the current cards on screen; the next scroll/recheck retries.
            setPaginationError(errorMessage(err, 'Could not load more cards'));
        } finally {
            loadingMoreRef.current = false;
            setIsLoadingMore(false);
        }
    }, [sessionExhausted, status]);

    const loadMore = useCallback(() => { void fetchMore(false); }, [fetchMore]);
    const checkForNewCards = useCallback(() => { void fetchMore(true); }, [fetchMore]);

    // While the session is exhausted and the feed is visible, periodically ask for
    // newly verified cards instead of requiring a manual refresh.
    useEffect(() => {
        if (!active || !sessionExhausted || status !== 'success') return;
        const timer = setInterval(checkForNewCards, Math.max(recheckSeconds, 30) * 1000);
        return () => clearInterval(timer);
    }, [active, sessionExhausted, status, recheckSeconds, checkForNewCards]);

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

        // Prefetch next batch when user gets within 3 cards of the bottom; at the
        // very last card of an exhausted session, check once for new cards.
        if (index >= cards.length - 3 && !sessionExhausted && !isLoadingMore) {
            loadMore();
        } else if (index === cards.length - 1 && sessionExhausted && !isLoadingMore) {
            checkForNewCards();
        }
    }, [cards, sessionExhausted, isLoadingMore, loadMore, checkForNewCards]);

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
        checkForNewCards,
        isLoadingMore,
        sessionExhausted,
        sessionComplete,
        paginationError,
    };
}
