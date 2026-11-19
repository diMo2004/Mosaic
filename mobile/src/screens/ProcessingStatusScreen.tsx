// Polls UPLOADED -> VERIFIED
import React, { useCallback, useEffect, useState } from 'react';
import { ActivityIndicator, Pressable, Text, View } from 'react-native';
import { getNoteStatus } from '@/api/notes';

const TERMINAL_STATUSES = new Set(['verified', 'failed']);

export default function ProcessingStatusScreen({ route, navigation }: any) {
    const noteId = route?.params?.noteId;
    const [note, setNote] = useState<any>(null);
    const [accessDenied, setAccessDenied] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchStatus = useCallback(async () => {
        if (!noteId) return;
        try {
            const data = await getNoteStatus(noteId);
            setNote(data);
            setError(null);
        } catch (err: any) {
            if (err.response?.status === 403 || err.response?.status === 404) {
                setAccessDenied(true);
                setError(err.response?.data?.detail || 'This note is not available on the signed-in account.');
                return;
            }
            setError(err.response?.data?.detail || err.message || 'Could not load note status.');
        }
    }, [noteId]);

    useEffect(() => {
        if (!noteId || accessDenied || TERMINAL_STATUSES.has(note?.status)) return;
        fetchStatus();
        const interval = setInterval(fetchStatus, 3000);
        return () => clearInterval(interval);
    }, [accessDenied, fetchStatus, note?.status, noteId]);

    return (
        <View className="flex-1 bg-canvas p-5">
            <Text className="text-xl font-bold text-slate-50">Processing status</Text>
            {!noteId ? (
                <Text className="mt-4 text-slate-300">Open this screen from an uploaded note.</Text>
            ) : (
                <>
                    <Text className="mt-2 text-sm text-slate-400">Note #{noteId}</Text>
                    {error ? <Text className="mt-4 text-red-300">{error}</Text> : null}
                    {!accessDenied ? (
                        <>
                            <View className="mt-4 flex-row items-center gap-2">
                                {!note || !TERMINAL_STATUSES.has(note.status) ? (
                                    <ActivityIndicator color="#38bdf8" />
                                ) : null}
                                <Text className="text-base text-slate-100">
                                    Status: <Text className="font-bold">{note?.status || 'Loading...'}</Text>
                                </Text>
                            </View>
                            {note?.status === 'verified' ? (
                                <Text className="mt-3 text-slate-300">
                                    Processing is complete. Flashcards are created only from supported claims. Open View Claims to see what was extracted from this note, then return to the feed.
                                </Text>
                            ) : null}
                            {note?.status === 'failed' ? (
                                <Text className="mt-3 text-red-300">
                                    Processing failed{note.processing_error ? `: ${note.processing_error}` : '.'}
                                </Text>
                            ) : null}
                            <Text numberOfLines={6} className="mt-4 rounded-xl bg-slate-900 p-3 text-slate-200">
                                {note?.extracted_text || 'No text extracted yet...'}
                            </Text>
                            <Pressable onPress={fetchStatus} className="mt-4 items-center rounded-xl border border-slate-700 py-3">
                                <Text className="font-semibold text-slate-100">Refresh status</Text>
                            </Pressable>
                            <Pressable
                                onPress={() => navigation.navigate('ClaimReview', { noteId })}
                                className="mt-3 items-center rounded-xl bg-sky-500 py-3"
                            >
                                <Text className="font-bold text-slate-950">View claims</Text>
                            </Pressable>
                            {note?.status === 'verified' ? (
                                <Pressable
                                    onPress={() => navigation.navigate('Main')}
                                    className="mt-3 items-center rounded-xl border border-slate-700 py-3"
                                >
                                    <Text className="font-semibold text-sky-300">Back to feed</Text>
                                </Pressable>
                            ) : null}
                        </>
                    ) : null}
                </>
            )}
        </View>
    );
}
