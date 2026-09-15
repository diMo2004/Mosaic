// Feed, detail, save/unsave playlist, feedback, explain
import {apiClient} from './client';

export const getFlashcards = async () => {
    return (await apiClient.get('/api/learning/flashcards/')).data;
};

export const getFlashcardDetail = async (id: number) => {
    return (await apiClient.get(`/api/learning/flashcards/${id}/`)).data;
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