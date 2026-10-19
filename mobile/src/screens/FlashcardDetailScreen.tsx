// mobile/src/screens/FlashcardDetailScreen.tsx
// Dark-mode themed detail view for an individual flashcard.
import React, { useState, useEffect } from 'react';
import { View, Text, Alert, ScrollView, ActivityIndicator } from 'react-native';
import { Bookmark, BookOpen, Eye, ThumbsDown, ThumbsUp } from 'lucide-react-native';
import { getFlashcardDetail, sendFeedback } from '@/api/learning';
import { Badge, Button, Card, CardTitle } from '@/components/ui';

export default function FlashcardDetailScreen({ route, navigation }: any) {
    const { id } = route.params;
    const [card, setCard] = useState<any>(null);
    const [showAnswer, setShowAnswer] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getFlashcardDetail(id)
            .then(setCard)
            .catch((err) => Alert.alert('Error', err.message || 'Failed to load card.'))
            .finally(() => setLoading(false));
    }, [id]);

    const handleFeedback = async (type: 'like' | 'dislike') => {
        try {
            await sendFeedback(id, type);
            Alert.alert('Feedback sent', `You marked this card as ${type}.`);
        } catch (error: any) {
            Alert.alert('Feedback Error', error.response?.data?.detail || error.message);
        }
    };

    if (loading || !card) {
        return (
            <View className="flex-1 items-center justify-center bg-canvas">
                <ActivityIndicator size="large" color="#38bdf8" />
                <Text className="mt-3 text-sm text-slate-400">Loading card...</Text>
            </View>
        );
    }

    return (
        <ScrollView className="flex-1 bg-canvas p-5" contentContainerStyle={{ paddingBottom: 40 }}>
            {/* Concept & Difficulty Badges */}
            <View className="mb-4 flex-row items-center gap-2">
                <Badge variant="accent">{card.concept_name || 'Core Concept'}</Badge>
                <Badge variant="outline">{card.difficulty?.toUpperCase() || 'BEGINNER'}</Badge>
            </View>

            {/* Prompt Card */}
            <Card className="mb-4">
                <Text className="mb-2 text-xs font-bold uppercase tracking-wider text-sky-400">Question / Prompt</Text>
                <CardTitle className="text-lg leading-snug text-slate-100">{card.prompt}</CardTitle>
            </Card>

            {/* Answer & Explanation */}
            {showAnswer ? (
                <Card className="mb-4 border-sky-800/80 bg-slate-900/80">
                    <Text className="mb-2 text-xs font-bold uppercase tracking-wider text-emerald-400">Answer</Text>
                    <Text className="text-base font-semibold leading-relaxed text-slate-100">{card.answer}</Text>
                    {card.explanation ? (
                        <View className="mt-3.5 border-t border-slate-800 pt-3">
                            <Text className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">Explanation</Text>
                            <Text className="text-sm leading-relaxed text-slate-300 italic">{card.explanation}</Text>
                        </View>
                    ) : null}
                </Card>
            ) : (
                <Button
                    variant="secondary"
                    onPress={() => setShowAnswer(true)}
                    className="mb-4 py-4"
                >
                    <Eye size={18} color="#38bdf8" className="mr-2" />
                    Reveal Answer
                </Button>
            )}

            {/* Feedback Actions */}
            <View className="mb-4 flex-row gap-3">
                <Button
                    variant="outline"
                    onPress={() => handleFeedback('like')}
                    className="flex-1 flex-row items-center justify-center gap-2"
                >
                    <ThumbsUp size={16} color="#38bdf8" />
                    Helpful
                </Button>
                <Button
                    variant="outline"
                    onPress={() => handleFeedback('dislike')}
                    className="flex-1 flex-row items-center justify-center gap-2"
                >
                    <ThumbsDown size={16} color="#f87171" />
                    Not Helpful
                </Button>
            </View>

            {/* Save to Playlist Button */}
            <Button
                variant="secondary"
                onPress={() => navigation.navigate('PlaylistModal', { flashcardId: card.id })}
                className="mb-3 flex-row items-center justify-center gap-2"
            >
                <Bookmark size={18} color="#f59e0b" />
                Save to Playlist
            </Button>

            {/* Grounded Explanation Deep Link */}
            {card.canonical_claim_id ? (
                <Button
                    variant="default"
                    onPress={() => navigation.navigate('GroundedExplain', { claimId: card.canonical_claim_id })}
                    className="flex-row items-center justify-center gap-2"
                >
                    <BookOpen size={18} color="#020617" />
                    Grounded Source Explanation
                </Button>
            ) : null}
        </ScrollView>
    );
}