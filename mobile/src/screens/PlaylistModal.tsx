// Save to named playlist (not boolean)
// Opens bottom sheet with user's playlists; user taps to add/remove from playlist.
// Backend Endpoint: POST /api/learning/flashcards/{id}/save, GET /api/learning/playlists/

import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TextInput, Button, Alert } from 'react-native';
import { getPlaylists, createPlaylist, saveFlashcard, unsaveFlashcard } from '@/api/learning';

export default function PlaylistModal({ route, navigation }: any) {
    const { flashcardId } = route.params || {};
    const [playlists, setPlaylists] = useState<any[]>([]);
    const [newPlaylistName, setNewPlaylistName] = useState('');

    const loadPlaylists = async () => {
        const data = await getPlaylists();
        setPlaylists(data.results || data);
    };

    useEffect(() => {
        loadPlaylists();
    }, []);

    const handleCreate = async () => {
        if (!newPlaylistName.trim())
            return;
        await createPlaylist(newPlaylistName.trim());
        setNewPlaylistName('');
        loadPlaylists();
    };

    const handleSave = async (playlistId: number) => {
        await saveFlashcard(flashcardId, playlistId);
        Alert.alert('Saved', 'Flashcard added to playlist!');
        navigation.goBack();
    };

    const handleUnsave = async (playlistId: number) => {
        await unsaveFlashcard(flashcardId, playlistId);
        Alert.alert('Unsaved', 'Flashcard removed from playlist!');
        navigation.goBack();
    };

    return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Named Playlists</Text>
      <View style={{ flexDirection: 'row', marginVertical: 10 }}>
        <TextInput
          placeholder="New playlist name"
          value={newPlaylistName}
          onChangeText={setNewPlaylistName}
          style={{ borderWidth: 1, flex: 1, padding: 6, marginRight: 6 }}
        />
        <Button title="Create" onPress={handleCreate} />
      </View>
      <FlatList
        data={playlists}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <View style={{ padding: 10, borderBottomWidth: 1, borderColor: '#eee' }}>
            <Text style={{ fontWeight: 'bold' }}>{item.name} {item.is_default && '(Default)'}</Text>
            {flashcardId && (
              <View style={{ flexDirection: 'row', marginTop: 4 }}>
                <Button title="Add Here" onPress={() => handleSave(item.id)} />
                <View style={{ marginLeft: 10 }}>
                  <Button title="Remove" onPress={() => handleUnsave(item.id)} color="red" />
                </View>
              </View>
            )}
          </View>
        )}
      />
    </View>
  );
}