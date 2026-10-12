// Public flashcard feed
// Displays cards with concept tag, canonical claim, and provenance indicator.
// Backend Endpoint: GET /api/learning/feed/

import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, Button, Alert } from 'react-native';
import { getFlashcards } from '@/api/learning';

export default function FeedScreen({ navigation }: any) {
    const [cards, setCards] = useState<any[]>([]);
    const [needsProfile, setNeedsProfile] = useState(false);
    const loadFeed = async () => {
        setNeedsProfile(false);
        try {
            const res = await getFlashcards();
            setCards(Array.isArray(res) ? res :res.results || []);
        } catch (error: any) {
            if (error.response?.status === 403) {
                setNeedsProfile(true);
            } else {
                Alert.alert('Feed Error', JSON.stringify(error.response?.data || error.message));
            }
        }
    };

    useEffect(() => {
        loadFeed();
    }, []);

    return (
    <View style={{ padding: 20, flex: 1 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold', marginBottom: 10 }}>
        Public Flashcard Feed
      </Text>

      <Button title="Refresh Feed" onPress={loadFeed} />

      {needsProfile && (
        <View
          style={{
            padding: 16,
            backgroundColor: '#fef2f2',
            borderRadius: 8,
            marginVertical: 10,
          }}
        >
          <Text style={{ color: '#b91c1c', fontWeight: 'bold' }}>
            Profile Incomplete
          </Text>
          <Text style={{ marginVertical: 6 }}>
            Please complete your profile to unlock flashcards.
          </Text>
          <Button
            title="Go to Complete Profile"
            onPress={() => navigation.navigate('CompleteProfile')}
          />
        </View>
      )}

      <FlatList
        data={cards}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <TouchableOpacity
            onPress={() =>
              navigation.navigate('FlashcardDetail', { id: item.id })
            }
            style={{
              padding: 12,
              borderWidth: 1,
              marginVertical: 6,
              borderRadius: 4,
            }}
          >
            <Text style={{ color: 'blue', fontWeight: 'bold' }}>
              [{item.concept_name}]
            </Text>
            <Text style={{ fontSize: 16, marginTop: 4 }}>
              {item.canonical_text || item.prompt}
            </Text>
            <Text style={{ fontSize: 12, color: '#666', marginTop: 4 }}>
              Difficulty: {item.difficulty} | Views: {item.view_count || 0}
            </Text>
          </TouchableOpacity>
        )}
      />
    </View>
  );
}