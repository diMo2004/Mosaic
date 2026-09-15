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
    return (await apiClient.post('/api/auth/register/', { username, email, password})).data;
};

export const completeProfile = async (data: { 
    full_name: string;
    education_level: string;
    learning_goal: string;
    interests?: string[];
}) => {
    return (await apiClient.post(`/api/auth/complete-profile/`, data)).data;
};

export const logout = async () => {
    await SecureStore.deleteItemAsync('accessToken');
    await SecureStore.deleteItemAsync('refreshToken');
};