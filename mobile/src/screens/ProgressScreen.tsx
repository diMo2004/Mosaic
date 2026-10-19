// Location: mobile/src/screens/ProgressScreen.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, ActivityIndicator, TextInput, Pressable } from 'react-native';
import { getProgressSummary, getUserBadges } from '../api/learning';

export default function ProgressScreen({ navigation }: any) {
    const [summary, setSummary] = useState<any>(null);
    const [badges, setBadges] = useState<any[]>([]);
    const [conceptIdInput, setConceptIdInput] = useState('');
    const [loading, setLoading] = useState(true);

    const loadData = async () => {
        setLoading(true);
        try {
            const sum = await getProgressSummary();
            const b = await getUserBadges();
            setSummary(sum);
            setBadges(b);
        } catch (e: any) {
            alert(e.message || 'Error loading progress');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    return (
        <View className="flex-1 bg-canvas p-5">
            <Pressable onPress={loadData} className="mb-4 items-center rounded-xl bg-sky-500 py-3"><Text className="font-bold text-slate-950">Refresh progress & badges</Text></Pressable>
            {loading ? <ActivityIndicator size="large" color="#38bdf8" /> : (
                <View className="flex-1">
                    {summary && (
                        <View className="my-3 rounded-xl border border-slate-800 bg-panel p-4">
                            <Text className="text-slate-200">Total viewed: {summary.total_flashcards_viewed}</Text>
                            <Text className="text-slate-200">Total views: {summary.total_views}</Text>
                            <Text className="text-slate-200">Understood: {summary.understood_count}</Text>
                            <Text className="text-slate-200">Saved cards: {summary.saved_count}</Text>
                        </View>
                    )}

                    <View className="my-3">
                        <Text className="font-bold text-slate-100">Test concept mastery</Text>
                        <TextInput
                            placeholder="Enter concept ID" placeholderTextColor="#64748b"
                            value={conceptIdInput}
                            onChangeText={setConceptIdInput}
                            keyboardType="numeric"
                            className="my-2 rounded-xl border border-slate-700 bg-slate-900 px-3 py-3 text-slate-50"
                        />
                        <Pressable onPress={() => {
                                if (!conceptIdInput) return alert('Enter a concept ID');
                                navigation.navigate('Mastery', { conceptId: Number(conceptIdInput) });
                            }} className="items-center rounded-xl border border-sky-700 py-3"><Text className="font-semibold text-sky-300">Open mastery questionnaire</Text></Pressable>
                    </View>

                    <Text className="mt-4 font-bold text-slate-100">Earned badges</Text>
                    <FlatList
                        data={badges}
                        keyExtractor={(item) => item.id.toString()}
                        renderItem={({ item }) => (
                            <View className="border-b border-slate-800 py-3">
                                <Text className="text-slate-100">🏅 {item.concept_name} {item.is_superset ? '(SUPERSET)' : ''}</Text>
                                <Text className="text-xs text-slate-400">Awarded: {item.completion_date}</Text>
                            </View>
                        )}
                        ListEmptyComponent={<Text className="text-slate-400">No badges earned yet.</Text>}
                    />
                </View>
            )}
        </View>
    );
}
