// Public flashcard feed
// Displays cards with concept tag, canonical claim, and provenance indicator.
// Backend Endpoint: GET /api/learning/feed/

import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, Button, Alert } from 'react-native';
import { getFlashcards } from '@/api/learning';

export default function FeedScreen({ navigation }: any) {
    const [cards, setCards] = useState<any[]>([]);
    const loadFeed = async () => {
        try {
            const res = await getFlashcards();
            setCards(res.results || res);
        } catch (error: any) {
            Alert.alert('Feed Error', JSON.stringify(error.response?.data || error.message));
        }
    };

    useEffect(() => {
        loadFeed();
    }, []);

    return (
    <View style={{ padding: 20, flex: 1 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold', marginBottom: 10 }}>Public Flashcard Feed</Text>
      <Button title="Refresh Feed" onPress={loadFeed} />
      <FlatList
        data={cards}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <TouchableOpacity
            onPress={() => navigation.navigate('FlashcardDetail', { id: item.id })}
            style={{ padding: 12, borderWidth: 1, marginVertical: 6, borderRadius: 4 }}
          >
            <Text style={{ color: 'blue', fontWeight: 'bold' }}>[{item.concept_name}]</Text>
            <Text style={{ fontSize: 16, marginTop: 4 }}>{item.canonical_text || item.prompt}</Text>
            <Text style={{ fontSize: 12, color: '#666', marginTop: 4 }}>
              Difficulty: {item.difficulty} | Views: {item.view_count || 0}
            </Text>
          </TouchableOpacity>
        )}
      />
    </View>
  );
}