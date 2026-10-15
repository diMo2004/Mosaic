// Feed, detail, save/unsave playlist, feedback, explain
import {apiClient} from './client';
import type { FlashcardDTO, FlashcardListResponse } from '@/types/flashcard';

export const getFlashcards = async (): Promise<FlashcardListResponse> => {
    return (await apiClient.get<FlashcardListResponse>('/api/learning/flashcards/')).data;
};

export const getFlashcardDetail = async (id: number): Promise<FlashcardDTO> => {
    return (await apiClient.get<FlashcardDTO>(`/api/learning/flashcards/${id}/`)).data;
};

export const getPlaylists = async () => {
    return (await apiClient.get('/api/learning/playlists/')).data;
}

export const createPlaylist = async (name: string) => {
    return (await apiClient.post('/api/learning/playlists/', {name})).data;
};

export const saveFlashcard = async (flashcardId: number, playlistId?: number) => {
    return (await apiClient.post(`/api/learning/flashcards/${flashcardId}/save/`, {
        playlist_id: playlistId,
    })).data;
};

export const unsaveFlashcard = async (flashcardId: number, playlistId?: number) => {
    const url = playlistId
    ? `/api/learning/flashcards/${flashcardId}/save/?playlist_id=${playlistId}`
    : `/api/learning/flashcards/${flashcardId}/save/`;
    return (await apiClient.delete(url)).data;
};

export const sendFeedback = async (flashcardId: number, feedbackType: 'like' | 'dislike', comment: string = '') => {
    return (await apiClient.post(`/api/learning/flashcards/${flashcardId}/feedback/`, {
        feedback_type: feedbackType,
        comment,
    })).data;
};

export const getExplanation = async (canonicalClaimId: number) => {
    return (await apiClient.get(`/api/learning/canonical-claims/${canonicalClaimId}/explain/`)).data;
};

export const markFlashcardUnderstood = async (flashcardId: number, understood: boolean = true) => {
    return (await apiClient.post(`/api/learning/flashcards/${flashcardId}/understood/`, { understood
    })).data;
};

export const getProgressSummary = async () => {
    return (await apiClient.get('/api/learning/progress/')).data;
};

export const getMasteryStatus = async (conceptId: number) => {
    return (await apiClient.get(`/api/learning/concepts/${conceptId}/mastery-status/`)).data;
};

export const startQuestionnaire = async (conceptId: number) => {
    return (await apiClient.post(`/api/learning/concepts/${conceptId}/questionnaires/start/`)).data;
};
export const submitQuestionnaire = async (questionnaireId: number, answers: { question_id: number; selected_option: number }[]) => {
    return (await apiClient.post(`/api/learning/questionnaires/${questionnaireId}/submit/`, { answers })).data;
};
export const getUserBadges = async () => {
    return (await apiClient.get('/api/learning/badges/')).data;
};