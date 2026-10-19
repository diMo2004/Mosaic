import React, { useState } from 'react';
import { ActivityIndicator, Pressable, ScrollView, Text, View } from 'react-native';
import { AlertCircle, CheckCircle2, Search, Sparkles } from 'lucide-react-native';
import { searchFlashcardsByTopic } from '@/api/learning';
import type { TopicSearchResponse } from '@/types/flashcard';
import { ScreenHeader } from '@/components/ScreenHeader';
import { Badge, Button, Card, CardContent, CardTitle, Input } from '@/components/ui';

export default function SearchScreen({ navigation }: any) {
  const [topic, setTopic] = useState('');
  const [result, setResult] = useState<TopicSearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const search = async (value = topic) => {
    if (!value.trim()) return;
    setLoading(true);
    setError(null);
    try {
      setResult(await searchFlashcardsByTopic(value.trim()));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Search could not be completed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="flex-1 bg-canvas">
      <ScreenHeader title="Search" navigation={navigation} />
      <ScrollView keyboardShouldPersistTaps="handled" className="flex-1 px-5 pt-4">
        {/* Search Input Bar */}
        <View className="flex-row items-center gap-2">
          <View className="flex-1">
            <Input
              value={topic}
              onChangeText={setTopic}
              onSubmitEditing={() => search()}
              placeholder="Search a CSE topic or technology"
              returnKeyType="search"
            />
          </View>
          <Button onPress={() => search()} loading={loading} className="px-5">
            <Search size={18} color="#020617" />
          </Button>
        </View>

        {error && (
          <View className="mt-4 flex-row items-center gap-2 rounded-xl border border-red-800 bg-red-950/60 p-4">
            <AlertCircle size={18} color="#f87171" />
            <Text className="text-sm font-medium text-red-200">{error}</Text>
          </View>
        )}

        {result && (
          <View className="mt-6 gap-4 pb-12">
            {/* Taxonomy Match Status Banner */}
            {result.taxonomy_match.found ? (
              <View className="flex-row items-center justify-between rounded-xl border border-emerald-800 bg-emerald-950/40 px-4 py-3">
                <View className="flex-row items-center gap-2">
                  <CheckCircle2 size={16} color="#34d399" />
                  <Text className="text-sm font-semibold text-emerald-200">
                    Taxonomy Concept: {result.taxonomy_match.name}
                  </Text>
                </View>
                {result.taxonomy_match.confidence && (
                  <Badge variant="success">
                    {Math.round(result.taxonomy_match.confidence * 100)}% match
                  </Badge>
                )}
              </View>
            ) : (
              <View className="rounded-xl border border-amber-800/80 bg-amber-950/30 p-4">
                <View className="flex-row items-center gap-2">
                  <Sparkles size={16} color="#fbbf24" />
                  <Text className="text-sm font-semibold text-amber-200">
                    "{result.query}" is not in the taxonomy
                  </Text>
                </View>
                <Text className="mt-1 text-xs text-amber-300/80">
                  Showing related concept flashcards and close matches below.
                </Text>
              </View>
            )}

            {/* Related Taxonomy Topic Suggestions */}
            {result.suggestions.length > 0 && (
              <View className="mt-1">
                <Text className="mb-2.5 text-xs font-bold uppercase tracking-wider text-slate-400">
                  Related Topics
                </Text>
                <View className="flex-row flex-wrap gap-2">
                  {result.suggestions.map(s => (
                    <Pressable
                      key={s.concept_id}
                      onPress={() => {
                        setTopic(s.name);
                        search(s.name);
                      }}
                      className="rounded-full border border-sky-800 bg-sky-950/60 px-3.5 py-1.5 active:bg-sky-900"
                    >
                      <Text className="text-xs font-semibold text-sky-200">
                        {s.name} {s.score ? `(${Math.round(s.score * 100)}%)` : ''}
                      </Text>
                    </Pressable>
                  ))}
                </View>
              </View>
            )}

            {/* Resulting Flashcards */}
            <View className="mt-2">
              <View className="mb-3 flex-row items-center justify-between">
                <Text className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Matching Flashcards
                </Text>
                <Badge variant="accent">{result.results.length} cards</Badge>
              </View>

              {result.results.length === 0 ? (
                <Card className="items-center py-8">
                  <Text className="text-base font-semibold text-slate-300">No cards generated for this topic yet</Text>
                  <Text className="mt-1 text-center text-xs text-slate-500">
                    Upload notes or ingest knowledge about this topic to populate flashcards.
                  </Text>
                </Card>
              ) : (
                <View className="gap-3">
                  {result.results.map(card => (
                    <Pressable
                      key={card.id}
                      onPress={() => navigation.navigate('FlashcardDetail', { id: card.id })}
                    >
                      <Card className="active:border-sky-500/50 active:bg-slate-900">
                        <View className="mb-2 flex-row items-center justify-between">
                          <Badge variant="accent">{card.concept_name || 'Concept'}</Badge>
                          <Badge variant="outline">{card.difficulty?.toUpperCase() || 'BEGINNER'}</Badge>
                        </View>
                        <CardTitle className="text-base font-bold text-slate-100">{card.prompt}</CardTitle>
                        <Text numberOfLines={2} className="mt-2 text-xs leading-relaxed text-slate-400">
                          {card.answer}
                        </Text>
                      </Card>
                    </Pressable>
                  ))}
                </View>
              )}
            </View>
          </View>
        )}
      </ScrollView>
    </View>
  );
}
