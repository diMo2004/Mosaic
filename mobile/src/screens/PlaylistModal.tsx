// mobile/src/screens/PlaylistModal.tsx
// Playlists manager: allows creating playlists, saving/unsaving flashcards,
// and tapping a playlist to browse its saved cards.
import React, { useEffect, useState, useCallback } from 'react';
import { View, Text, FlatList, Alert, Pressable } from 'react-native';
import { ChevronRight, FolderPlus, ListMusic } from 'lucide-react-native';
import { getPlaylists, createPlaylist, saveFlashcard, unsaveFlashcard } from '@/api/learning';
import { Badge, Button, Card, CardTitle, Input } from '@/components/ui';

export default function PlaylistModal({ route, navigation }: any) {
    const { flashcardId } = route.params || {};
    const [playlists, setPlaylists] = useState<any[]>([]);
    const [newPlaylistName, setNewPlaylistName] = useState('');
    const [creating, setCreating] = useState(false);

    const loadPlaylists = useCallback(async () => {
        try {
            const data = await getPlaylists();
            setPlaylists(data.results || data);
        } catch (error: any) {
            Alert.alert('Error', error.response?.data?.detail || error.message);
        }
    }, []);

    useEffect(() => {
        loadPlaylists();
    }, [loadPlaylists]);

    const handleCreate = async () => {
        if (!newPlaylistName.trim()) return;
        setCreating(true);
        try {
            await createPlaylist(newPlaylistName.trim());
            setNewPlaylistName('');
            loadPlaylists();
        } catch (error: any) {
            Alert.alert('Error', error.response?.data?.detail || error.message);
        } finally {
            setCreating(false);
        }
    };

    const handleSave = async (playlistId: number) => {
        try {
            await saveFlashcard(flashcardId, playlistId);
            Alert.alert('Saved', 'Flashcard added to playlist!');
            navigation.goBack();
        } catch (error: any) {
            Alert.alert('Error', error.response?.data?.detail || error.message);
        }
    };

    const handleUnsave = async (playlistId: number) => {
        try {
            await unsaveFlashcard(flashcardId, playlistId);
            Alert.alert('Unsaved', 'Flashcard removed from playlist!');
            navigation.goBack();
        } catch (error: any) {
            Alert.alert('Error', error.response?.data?.detail || error.message);
        }
    };

    return (
        <View className="flex-1 bg-canvas p-5">
            <View className="mb-4">
                <Text className="text-xl font-bold text-slate-50">
                    {flashcardId ? 'Save to Playlist' : 'Your Playlists'}
                </Text>
                <Text className="mt-1 text-xs text-slate-400">
                    {flashcardId
                        ? 'Select a playlist to store this flashcard for future review.'
                        : 'Manage your study lists and tap any playlist to review its saved cards.'}
                </Text>
            </View>

            {/* Create Playlist Input */}
            <View className="mb-5 flex-row items-center gap-2">
                <View className="flex-1">
                    <Input
                        placeholder="New playlist name..."
                        value={newPlaylistName}
                        onChangeText={setNewPlaylistName}
                    />
                </View>
                <Button onPress={handleCreate} loading={creating} className="px-4">
                    <FolderPlus size={18} color="#020617" />
                </Button>
            </View>

            <FlatList
                data={playlists}
                keyExtractor={(item) => String(item.id)}
                contentContainerStyle={{ gap: 12, paddingBottom: 24 }}
                renderItem={({ item }) => (
                    <Card className="active:border-sky-500/50 active:bg-slate-900">
                        <Pressable
                            onPress={() => {
                                if (!flashcardId) {
                                    navigation.navigate('PlaylistDetail', {
                                        playlistId: item.id,
                                        playlistName: item.name,
                                    });
                                }
                            }}
                            className="flex-row items-center justify-between"
                        >
                            <View className="flex-1">
                                <View className="flex-row items-center gap-2">
                                    <CardTitle className="text-base text-slate-100">{item.name}</CardTitle>
                                    {item.is_default && <Badge variant="accent">Default</Badge>}
                                </View>
                                <Text className="mt-1 text-xs text-slate-400">
                                    {item.item_count ?? 0} saved cards
                                </Text>
                            </View>
                            {!flashcardId && <ChevronRight size={20} color="#64748b" />}
                        </Pressable>

                        {flashcardId && (
                            <View className="mt-3.5 flex-row gap-2.5 pt-3 border-t border-slate-800">
                                <Button
                                    size="sm"
                                    onPress={() => handleSave(item.id)}
                                    className="flex-1"
                                >
                                    Add Here
                                </Button>
                                <Button
                                    variant="outline"
                                    size="sm"
                                    onPress={() => handleUnsave(item.id)}
                                    className="border-red-800 active:bg-red-950/40"
                                    textClassName="text-red-400"
                                >
                                    Remove
                                </Button>
                            </View>
                        )}
                    </Card>
                )}
                ListEmptyComponent={
                    <View className="items-center py-12 px-4">
                        <ListMusic size={36} color="#475569" />
                        <Text className="mt-3 text-sm font-semibold text-slate-300">No playlists yet</Text>
                        <Text className="mt-1 text-xs text-slate-500">
                            Create your first playlist above to start organizing flashcards.
                        </Text>
                    </View>
                }
            />
        </View>
    );
}
