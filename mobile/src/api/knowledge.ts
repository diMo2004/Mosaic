import { apiClient } from './client';

export const getSources = async () => {
    return (await apiClient.get('/api/knowledge/sources/')).data;
};

export const getSourceDocuments = async () => {
    return (await apiClient.get('/api/knowledge/source-documents/')).data;
};

export const getCanonicalClaims = async () => {
    return (await apiClient.get('/api/knowledge/canonical-claims/')).data;
};

export const getEvidenceList = async () => {
    return (await apiClient.get('/api/knowledge/evidence/')).data;
}