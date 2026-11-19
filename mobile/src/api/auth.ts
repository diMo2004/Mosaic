// Login, register, Google, complete-profile
import { apiClient } from './client';
import { deleteStoredItem, setStoredItem } from './tokenStore';

export const login = async (username: string, password: string) => {
    const res = await apiClient.post('/api/auth/login/', { username, password });
    await setStoredItem('accessToken', res.data.access);
    await setStoredItem('refreshToken', res.data.refresh);
    return res.data;
};

export const register = async (username: string, email: string, password: string) => {
    const res = await apiClient.post('/api/auth/register/', { username, email, password });
    await setStoredItem('accessToken', res.data.access);
    await setStoredItem('refreshToken', res.data.refresh);
    return res.data;
};

export const completeProfile = async (data: { 
    full_name: string;
    education_level: string;
    learning_goal: string;
    interests?: string[];
}) => {
    const res = await apiClient.post('/api/auth/complete-profile/', data);
    if (res.data.access) {
        await setStoredItem('accessToken', res.data.access);
    }
    if (res.data.refresh) {
        await setStoredItem('refreshToken', res.data.refresh);
    }
    return res.data;
};

export const getProfile = async () => {
    return (await apiClient.get('/api/auth/complete-profile/')).data;
};

export const logout = async () => {
    await deleteStoredItem('accessToken');
    await deleteStoredItem('refreshToken');
};
