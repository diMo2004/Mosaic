// Location: mobile/src/screens/ProgressScreen.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, Button, FlatList, ActivityIndicator, TextInput } from 'react-native';
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
        <View style={{ flex: 1, padding: 16 }}>
            <Button title="Refresh Progress & Badges" onPress={loadData} />
            {loading ? <ActivityIndicator size="large" style={{ marginTop: 20 }} /> : (
                <View style={{ flex: 1 }}>
                    {summary && (
                        <View style={{ marginVertical: 12, padding: 12, backgroundColor: '#f5f5f5' }}>
                            <Text>Total Viewed: {summary.total_flashcards_viewed}</Text>
                            <Text>Total Views: {summary.total_views}</Text>
                            <Text>Understood Count: {summary.understood_count}</Text>
                            <Text>Saved Cards: {summary.saved_count}</Text>
                        </View>
                    )}

                    <View style={{ marginVertical: 12 }}>
                        <Text style={{ fontWeight: 'bold' }}>Test Concept Mastery:</Text>
                        <TextInput
                            placeholder="Enter Concept ID (e.g. 1)"
                            value={conceptIdInput}
                            onChangeText={setConceptIdInput}
                            keyboardType="numeric"
                            style={{ borderWidth: 1, borderColor: '#ccc', padding: 8, marginVertical: 8 }}
                        />
                        <Button
                            title="Go to Mastery & Questionnaire"
                            onPress={() => {
                                if (!conceptIdInput) return alert('Enter a concept ID');
                                navigation.navigate('Mastery', { conceptId: Number(conceptIdInput) });
                            }}
                        />
                    </View>

                    <Text style={{ fontWeight: 'bold', marginTop: 16 }}>Earned Badges:</Text>
                    <FlatList
                        data={badges}
                        keyExtractor={(item) => item.id.toString()}
                        renderItem={({ item }) => (
                            <View style={{ padding: 8, borderBottomWidth: 1, borderColor: '#ddd' }}>
                                <Text>🏅 {item.concept_name} {item.is_superset ? '(SUPERSET)' : ''}</Text>
                                <Text style={{ fontSize: 12, color: '#666' }}>Awarded: {item.completion_date}</Text>
                            </View>
                        )}
                        ListEmptyComponent={<Text>No badges earned yet.</Text>}
                    />
                </View>
            )}
        </View>
    );
}