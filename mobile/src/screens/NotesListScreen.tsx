import React, { useCallback, useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, ActivityIndicator, Pressable } from 'react-native';
import { getNotes } from '../api/notes';

export default function NotesListScreen({ navigation }: any) {
    const [notes, setNotes] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const load = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getNotes();
            setNotes(Array.isArray(data) ? data : data.results || []);
        } catch (err: any) {
            setError(err.response?.data?.detail || err.message || 'Failed to fetch notes.');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        load();
    }, [load]);

    return (
        <View className="flex-1 bg-canvas p-5">
            <Pressable onPress={load} className="mb-4 items-center rounded-xl bg-sky-500 py-3"><Text className="font-bold text-slate-950">Refresh notes</Text></Pressable>
            {loading ? <ActivityIndicator size="large" color="#38bdf8" /> : (
                error ? (
                    <View className="p-4">
                        <Text className="text-center text-red-300">{error}</Text>
                    </View>
                ) : (
                <FlatList
                    data={notes}
                    keyExtractor={(item) => item.id.toString()}
                    renderItem={({ item }) => (
                        <TouchableOpacity
                            onPress={() => navigation.navigate('ProcessingStatus', { noteId: item.id })}
                            className="border-b border-slate-800 py-4"
                        >
                            <Text className="font-bold text-slate-100">{item.title || 'Untitled'}</Text>
                            <Text className="mt-1 text-slate-400">Status: {item.status}</Text>
                        </TouchableOpacity>
                    )}
                    ListEmptyComponent={<Text className="mt-5 text-center text-slate-400">No notes found.</Text>}
                />
                )
            )}
        </View>
    );
} 
