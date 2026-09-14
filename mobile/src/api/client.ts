// Axios instance + JWT refresh interceptor
import axios, {AxiosError, InternalAxiosRequestConfig} from 'axios';
import * as SecureStore from 'expo-secure-store';

const DEV_API_URL = 'http://10.0.2.2:8000'; //Android emulator localhost
const PROD_API_URL = 'https://mosaic-backend-n8a9.onrender.com';

export const BASE_URL = process.env.EXPO_BASE_URL || (__DEV__ ? DEV_API_URL : PROD_API_URL);

export const apiClient = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'applicaton/json',
        Accept: 'application/json',
    },
    timeout: 15000,
});

apiClient.interceptors.request.use(
    async (config: InternalAxiosRequestConfig) => {
        try {
            const accessToken = await SecureStore.getItemAsync('accessToken');
            if (accessToken && config.headers) {
                config.headers.Authorization = `Bearer ${accessToken}`;
            }
        }
        catch (error) {
            console.error('[API Client] Error reading access_token from SecureStore', error);
        }
        return config;
    },
    (error) => Promise.reject(error)
);

interface CustomAxiosRequestConfig extends InternalAxiosRequestConfig {
    _retry?: boolean;
}

apiClient.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const originalRequest = error.config as CustomAxiosRequestConfig;
        if (error.response?.status === 401 && originalRequest && !originalRequest._retry &&
            !originalRequest.url?.includes('/api/auth/token/refresh/') &&
            !originalRequest.url?.includes('/api/auth/login/')) {
            originalRequest._retry = true;
            try {
                const refreshToken = await SecureStore.getItemAsync('refreshToken');
                if (!refreshToken) {
                    throw new Error('No refresh token available');
                }

                const refreshResponse = await axios.post(`${BASE_URL}/api/auth/token/refresh/`, {
                    refresh: refreshToken,
                });
                
                const newAccessToken = refreshResponse.data.access;
                await SecureStore.setItemAsync('accessToken', newAccessToken);

                if (refreshResponse.data.refresh) {
                    await SecureStore.setItemAsync('refreshToken', refreshResponse.data.refresh);
                }
                if (originalRequest.headers) {
                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                }
                return apiClient(originalRequest);
            } catch (refreshError) {
                await SecureStore.deleteItemAsync('accessToken');
                await SecureStore.deleteItemAsync('refreshToken');
                console.error('[API Client] Token refresh failed', refreshError);
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
)