import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';

const webMemory = new Map<string, string>();

function webGet(key: string): string | null {
    try {
        return globalThis.localStorage?.getItem(key) ?? webMemory.get(key) ?? null;
    } catch {
        return webMemory.get(key) ?? null;
    }
}

function webSet(key: string, value: string) {
    try {
        globalThis.localStorage?.setItem(key, value);
    } catch {
        webMemory.set(key, value);
    }
}

function webDelete(key: string) {
    try {
        globalThis.localStorage?.removeItem(key);
    } catch {
        webMemory.delete(key);
    }
}

export async function getStoredItem(key: string): Promise<string | null> {
    if (Platform.OS === 'web') return webGet(key);
    return SecureStore.getItemAsync(key);
}

export async function setStoredItem(key: string, value: string): Promise<void> {
    if (Platform.OS === 'web') {
        webSet(key, value);
        return;
    }
    await SecureStore.setItemAsync(key, value);
}

export async function deleteStoredItem(key: string): Promise<void> {
    if (Platform.OS === 'web') {
        webDelete(key);
        return;
    }
    await SecureStore.deleteItemAsync(key);
}
