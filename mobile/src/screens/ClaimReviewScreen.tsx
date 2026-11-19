// Review extracted claims
import React, { useCallback, useEffect, useState } from 'react';
import { ActivityIndicator, FlatList, Pressable, Text, View } from 'react-native';
import { getExtractedClaims, verifyClaim } from '@/api/notes';
import { apiErrorMessage, notify } from '@/utils/notify';

export default function ClaimReviewScreen({ route }: any) {
    const noteId = route?.params?.noteId;
    const [claims, setClaims] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [verifyingId, setVerifyingId] = useState<number | null>(null);

    const loadClaims = useCallback(async () => {
        if (!noteId) {
            setLoading(false);
            setError('No note was selected.');
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const data = await getExtractedClaims(noteId);
            setClaims(Array.isArray(data) ? data : data.results || []);
        } catch (err: any) {
            const status = err.response?.status;
            setError(
                status === 404
                    ? 'Claim review is not available on the deployed API yet. Redeploy the backend from this branch, then try again.'
                    : err.response?.data?.detail || err.message || 'Could not load claims.',
            );
        } finally {
            setLoading(false);
        }
    }, [noteId]);

    useEffect(() => {
        loadClaims();
    }, [loadClaims]);

    const handleVerify = async (id: number) => {
        setVerifyingId(id);
        try {
            const res = await verifyClaim(id);
            notify('Verification result', `Status: ${res.status}\nConfidence: ${res.confidence}`);
            loadClaims();
        } catch (err: any) {
            notify('Verification error', apiErrorMessage(err, 'Verification failed.'));
        } finally {
            setVerifyingId(null);
        }
    };

    return (
        <View className="flex-1 bg-canvas p-5">
            <Text className="mb-1 text-xl font-bold text-slate-50">Extracted claims</Text>
            <Text className="mb-4 text-sm text-slate-400">
                {noteId ? `From note #${noteId}` : 'No note selected'}
            </Text>
            <Pressable onPress={loadClaims} className="mb-4 items-center rounded-xl border border-slate-700 py-3">
                <Text className="font-semibold text-slate-100">Refresh claims</Text>
            </Pressable>
            {loading ? <ActivityIndicator color="#38bdf8" /> : null}
            {error ? <Text className="mb-3 text-red-300">{error}</Text> : null}
            <FlatList
                data={claims}
                keyExtractor={(item) => String(item.id)}
                ListEmptyComponent={
                    !loading && !error ? (
                        <Text className="mt-4 text-center text-slate-400">No claims extracted from this note yet.</Text>
                    ) : null
                }
                renderItem={({ item }) => (
                    <View className="mb-3 rounded-xl border border-slate-800 bg-slate-900 p-3">
                        <Text className="font-semibold text-slate-100">#{item.id}: {item.text}</Text>
                        <Text className="mt-1 text-slate-400">Status: {item.status} | Confidence: {item.confidence}</Text>
                        <Pressable
                            onPress={() => handleVerify(item.id)}
                            disabled={verifyingId === item.id}
                            className="mt-3 items-center rounded-lg bg-sky-500 py-2 disabled:opacity-50"
                        >
                            <Text className="font-bold text-slate-950">
                                {verifyingId === item.id ? 'Verifying…' : 'Run verification'}
                            </Text>
                        </Pressable>
                    </View>
                )}
            />
        </View>
    );
}
