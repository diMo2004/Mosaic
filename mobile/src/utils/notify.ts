import { Alert, Platform } from 'react-native';

// react-native-web's Alert.alert is a no-op, so messages would silently vanish on web.
export function notify(title: string, message?: string) {
    if (Platform.OS === 'web') {
        globalThis.alert?.(message ? `${title}\n\n${message}` : title);
        return;
    }
    Alert.alert(title, message);
}

export function apiErrorMessage(error: any, fallback: string): string {
    const data = error?.response?.data;
    if (!data) return error?.message || fallback;
    if (typeof data === 'string') return data.slice(0, 300);
    if (typeof data.detail === 'string') return data.detail;
    const fieldErrors = Object.entries(data)
        .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : String(messages)}`)
        .join('\n');
    return fieldErrors || fallback;
}
