// Front/back flip & stats
import React, { useState, useEffect } from 'react';
import { View, Text, Button, Alert, ScrollView } from 'react-native';
import { getFlashcardDetail, sendFeedback } from '@/api/learning';

export default function FlashcardDetailScreen({ route, navigation }: any) {
    const { id } = route.params;
    const [card, setCard] = useState<any>(null);
    const [showAnswer, setShowAnswer] = useState(false);

    useEffect(() => {
        getFlashcardDetail(id).then(setCard).catch(console.error);
    }, [id]);

    const handleFeedback = async (type: 'like' | 'dislike') => {
        try {
            await sendFeedback(id, type);
            Alert.alert('Feedback sent', `You marked this card as ${type}.`);
        } catch (error: any) {
            Alert.alert('Feedback Error', JSON.stringify(error.response?.data || error.message));
        }
    };

    if (!card) return <Text style={{ padding: 20 }}>Loading...</Text>;

    return (
    <ScrollView style={{ padding: 20 }}>
      <Text style={{ fontSize: 14, color: 'purple' }}>Concept: {card.concept_name}</Text>
      <Text style={{ fontSize: 18, fontWeight: 'bold', marginVertical: 10 }}>{card.prompt}</Text>
      {showAnswer ? (
        <View style={{ backgroundColor: '#f0f0f0', padding: 10, marginVertical: 10 }}>
          <Text style={{ fontSize: 16, fontWeight: 'bold' }}>Answer:</Text>
          <Text style={{ marginTop: 4 }}>{card.answer}</Text>
          {card.explanation && <Text style={{ marginTop: 8, fontStyle: 'italic' }}>{card.explanation}</Text>}
        </View>
      ) : (
        <Button title="Reveal Answer" onPress={() => setShowAnswer(true)} />
      )}
      <View style={{ flexDirection: 'row', justifyContent: 'space-around', marginVertical: 15 }}>
        <Button title="👍 Like" onPress={() => handleFeedback('like')} />
        <Button title="👎 Dislike" onPress={() => handleFeedback('dislike')} />
      </View>
      <View style={{ marginTop: 10 }}>
        <Button
          title="Save to Playlist"
          onPress={() => navigation.navigate('PlaylistModal', { flashcardId: card.id })}
        />
      </View>
      {card.canonical_claim_id && (
        <View style={{ marginTop: 10 }}>
          <Button
            title="In-Depth Grounded Explanation"
            onPress={() => navigation.navigate('GroundedExplain', { claimId: card.canonical_claim_id })}
          />
        </View>
      )}
    </ScrollView>
  );
}