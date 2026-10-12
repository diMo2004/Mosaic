// Location: mobile/src/screens/MasteryScreen.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, Button, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { getMasteryStatus, startQuestionnaire, submitQuestionnaire } from '../api/learning';

export default function MasteryScreen({ route }: any) {
    const { conceptId } = route.params;
    const [status, setStatus] = useState<any>(null);
    const [questionnaire, setQuestionnaire] = useState<any>(null);
    const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({});
    const [submitResult, setSubmitResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const loadStatus = async () => {
        setLoading(true);
        try {
            const data = await getMasteryStatus(conceptId);
            setStatus(data);
        } catch (e: any) {
            alert(e.message || 'Status check failed');
        } finally {
            setLoading(false);
        }
    };

    const handleStart = async () => {
        setLoading(true);
        setSubmitResult(null);
        setSelectedAnswers({});
        try {
            const data = await startQuestionnaire(conceptId);
            setQuestionnaire(data);
        } catch (e: any) {
            alert(e.message || 'Failed to start questionnaire');
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async () => {
        if (!questionnaire) return;
        const answers = Object.entries(selectedAnswers).map(([qid, opt]) => ({
            question_id: Number(qid),
            selected_option: opt,
        }));
        setLoading(true);
        try {
            const res = await submitQuestionnaire(questionnaire.questionnaire_id, answers);
            setSubmitResult(res);
            setQuestionnaire(null);
            loadStatus(); // refresh tier status
        } catch (e: any) {
            alert(e.message || 'Submission failed');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadStatus();
    }, [conceptId]);

    if (loading) return <ActivityIndicator size="large" style={{ marginTop: 40 }} />;

    return (
        <ScrollView style={{ flex: 1, padding: 16 }}>
            {status && (
                <View style={{ marginBottom: 16, padding: 12, backgroundColor: '#eee' }}>
                    <Text style={{ fontWeight: 'bold', fontSize: 16 }}>{status.concept_name}</Text>
                    <Text>Current Tier: {status.current_tier} / 5</Text>
                    <Text>Eligible for Next Tier: {status.eligibility?.eligible ? 'YES' : 'NO'}</Text>
                    {!status.eligibility?.eligible && (
                        <Text style={{ color: 'red' }}>Reason: {status.eligibility?.reason}</Text>
                    )}
                    <Text>Fully Mastered: {status.is_mastered ? 'YES' : 'NO'}</Text>
                </View>
            )}

            {!questionnaire && !submitResult && (
                <Button title="Start Tier Questionnaire" onPress={handleStart} />
            )}

            {questionnaire && (
                <View>
                    <Text style={{ fontSize: 16, fontWeight: 'bold', marginVertical: 8 }}>
                        Tier {questionnaire.tier} Test (Pass: {questionnaire.passing_threshold}/10)
                    </Text>
                    {questionnaire.questions.map((q: any, qIdx: number) => (
                        <View key={q.id} style={{ marginVertical: 8, padding: 8, borderWidth: 1, borderColor: '#ccc' }}>
                            <Text style={{ fontWeight: 'bold' }}>Q{qIdx + 1}: {q.prompt}</Text>
                            {q.options.map((opt: string, optIdx: number) => {
                                const isSelected = selectedAnswers[q.id] === optIdx;
                                return (
                                    <TouchableOpacity
                                        key={optIdx}
                                        onPress={() => setSelectedAnswers({ ...selectedAnswers, [q.id]: optIdx })}
                                        style={{
                                            padding: 8,
                                            marginVertical: 4,
                                            backgroundColor: isSelected ? '#bbf7d0' : '#f3f4f6',
                                        }}
                                    >
                                        <Text>{optIdx + 1}. {opt}</Text>
                                    </TouchableOpacity>
                                );
                            })}
                        </View>
                    ))}
                    <Button title="Submit Answers" onPress={handleSubmit} />
                </View>
            )}

            {submitResult && (
                <View style={{ marginTop: 16, padding: 12, backgroundColor: '#fef08a' }}>
                    <Text style={{ fontWeight: 'bold', fontSize: 18 }}>
                        Result: {submitResult.passed ? 'PASSED! 🎉' : 'FAILED'}
                    </Text>
                    <Text>Score: {submitResult.score} / {submitResult.total}</Text>
                    <Text>New Current Tier: {submitResult.new_tier}</Text>
                    {submitResult.badge_awarded && <Text style={{ color: 'green', fontWeight: 'bold' }}>New Badge Awarded!</Text>}
                    <View style={{ marginTop: 10 }}>
                        <Button title="Take Another / Refresh" onPress={loadStatus} />
                    </View>
                </View>
            )}
        </ScrollView>
    );
}