// Login, register, Google, complete-profile
import { apiClient } from './client';
import * as SecureStore from 'expo-secure-store';

export const login = async (username: string, password: string) => {
    const res = await apiClient.post('/api/auth/login/', { username, password });
    await SecureStore.setItemAsync('accessToken', res.data.access);
    await SecureStore.setItemAsync('refreshToken', res.data.refresh);
    return res.data;
};

export const register = async (username: string, email: string, password: string) => {
    const res = await apiClient.post('/api/auth/register/', { username, email, password });
    await SecureStore.setItemAsync('accessToken', res.data.access);
    await SecureStore.setItemAsync('refreshToken', res.data.refresh);
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
        await SecureStore.setItemAsync('accessToken', res.data.access);
    }
    if (res.data.refresh) {
        await SecureStore.setItemAsync('refreshToken', res.data.refresh);
    }
    return res.data;
};

export const getProfile = async () => {
    return (await apiClient.get('/api/auth/complete-profile/')).data;
};

export const logout = async () => {
    await SecureStore.deleteItemAsync('accessToken');
    await SecureStore.deleteItemAsync('refreshToken');
};
