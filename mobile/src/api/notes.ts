// Multipart upload, fetch note status
import { Platform } from 'react-native';
import { apiClient } from './client';

export interface PickedNoteFile {
    uri: string;
    name: string;
    mimeType?: string | null;
    file?: File | null;
}

export const uploadNote = async (title: string, picked: PickedNoteFile) => {
    const formData = new FormData();
    formData.append('title', title);
    const type = picked.mimeType || 'text/plain';
    if (Platform.OS === 'web') {
        // Browsers need a real File/Blob; the React Native {uri, name, type} shape
        // is serialized as "[object Object]" and the server sees no file.
        const blob = picked.file ?? await (await fetch(picked.uri)).blob();
        formData.append('file', blob, picked.name);
    } else {
        formData.append('file', { uri: picked.uri, name: picked.name, type } as any);
    }

    return (await apiClient.post('/api/notes/upload/', formData, {
        // Leave Content-Type unset so the platform can add the multipart boundary.
        timeout: 120000,
    })).data;
};

export const getNoteStatus = async (noteId: number) => {
    return (await apiClient.get(`/api/notes/${noteId}/`)).data;
};

export const getExtractedClaims = async (noteId: number) => {
    return (await apiClient.get(`/api/notes/${noteId}/claims/`)).data;
};

export const verifyClaim = async (claimId: number) => {
    return (await apiClient.post(`/api/verification/claims/${claimId}/verify/`)).data;
};

export const getNotes = async () => {
    return (await apiClient.get('/api/notes/')).data;
};
