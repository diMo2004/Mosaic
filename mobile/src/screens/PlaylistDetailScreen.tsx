// mobile/src/screens/PlaylistDetailScreen.tsx
// Displays the flashcards saved within a specific playlist.
import React, { useEffect, useState, useCallback } from 'react';
import { View, Text, FlatList, Pressable, ActivityIndicator, Alert } from 'react-native';
import { ArrowLeft, BookOpen, Trash2 } from 'lucide-react-native';
import { getPlaylistDetail, unsaveFlashcard } from '@/api/learning';
import type { FlashcardDTO } from '@/types/flashcard';
import { Badge, Card, CardTitle } from '@/components/ui';

export default function PlaylistDetailScreen({ route, navigation }: any) {
    const { playlistId, playlistName } = route.params || {};
    const [playlist, setPlaylist] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    const loadDetail = useCallback(async () => {
        if (!playlistId) return;
        setLoading(true);
        try {
            const data = await getPlaylistDetail(playlistId);
            setPlaylist(data);
        } catch (error: any) {
            Alert.alert('Error', error.response?.data?.detail || error.message || 'Failed to load playlist.');
        } finally {
            setLoading(false);
        }
    }, [playlistId]);

    useEffect(() => {
        loadDetail();
    }, [loadDetail]);

    const handleRemoveCard = async (flashcardId: number) => {
        try {
            await unsaveFlashcard(flashcardId, playlistId);
            setPlaylist((prev: any) => ({
                ...prev,
                items: prev.items.filter((item: FlashcardDTO) => item.id !== flashcardId),
            }));
        } catch (error: any) {
            Alert.alert('Error', error.response?.data?.detail || error.message);
        }
    };

    return (
        <View className="flex-1 bg-canvas">
            {/* Top Bar */}
            <View className="flex-row items-center border-b border-slate-800 bg-slate-900/60 px-4 py-3.5">
                <Pressable
                    onPress={() => navigation.goBack()}
                    className="mr-3 rounded-full p-1.5 active:bg-slate-800"
                >
                    <ArrowLeft size={22} color="#f8fafc" />
                </Pressable>
                <View className="flex-1">
                    <Text className="text-lg font-bold text-slate-50">
                        {playlist?.name || playlistName || 'Playlist'}
                    </Text>
                    <Text className="text-xs text-slate-400">
                        {playlist?.items?.length ?? 0} saved cards
                    </Text>
                </View>
            </View>

            {loading ? (
                <View className="flex-1 items-center justify-center">
                    <ActivityIndicator size="large" color="#38bdf8" />
                    <Text className="mt-3 text-sm text-slate-400">Loading playlist...</Text>
                </View>
            ) : (
                <FlatList
                    data={playlist?.items || []}
                    keyExtractor={(item) => String(item.id)}
                    contentContainerStyle={{ padding: 16 }}
                    renderItem={({ item }: { item: FlashcardDTO }) => (
                        <Pressable
                            onPress={() => navigation.navigate('FlashcardDetail', { id: item.id })}
                            className="mb-3.5"
                        >
                            <Card className="active:bg-slate-900 active:border-sky-500/40">
                                <View className="mb-2 flex-row items-center justify-between">
                                    <Badge variant="accent">{item.concept_name || 'Concept'}</Badge>
                                    <Pressable
                                        onPress={() => handleRemoveCard(item.id)}
                                        className="rounded-lg p-1 active:bg-red-950/60"
                                        accessibilityLabel="Remove from playlist"
                                    >
                                        <Trash2 size={16} color="#ef4444" />
                                    </Pressable>
                                </View>
                                <CardTitle className="text-base font-bold text-slate-100">{item.prompt}</CardTitle>
                                <Text numberOfLines={2} className="mt-2 text-xs leading-relaxed text-slate-400">
                                    {item.answer}
                                </Text>
                            </Card>
                        </Pressable>
                    )}
                    ListEmptyComponent={
                        <View className="items-center py-16 px-4">
                            <BookOpen size={40} color="#475569" />
                            <Text className="mt-4 text-base font-bold text-slate-300">No cards in this playlist</Text>
                            <Text className="mt-1.5 text-center text-xs text-slate-500">
                                Save flashcards while exploring your feed to organize them here.
                            </Text>
                        </View>
                    }
                />
            )}
        </View>
    );
}
