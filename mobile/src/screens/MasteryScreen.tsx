// Location: mobile/src/screens/MasteryScreen.tsx
// Concept Mastery and Tier Progression testing screen.
import React, { useEffect, useState, useCallback } from 'react';
import { View, Text, ScrollView, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { Award, CheckCircle2, ChevronRight, HelpCircle, XCircle } from 'lucide-react-native';
import { getMasteryStatus, startQuestionnaire, submitQuestionnaire } from '../api/learning';
import { Badge, Button, Card, CardTitle } from '@/components/ui';

export default function MasteryScreen({ route, navigation }: any) {
    const { conceptId } = route.params;
    const [status, setStatus] = useState<any>(null);
    const [questionnaire, setQuestionnaire] = useState<any>(null);
    const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({});
    const [submitResult, setSubmitResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const loadStatus = useCallback(async () => {
        setLoading(true);
        try {
            const data = await getMasteryStatus(conceptId);
            setStatus(data);
        } catch (e: any) {
            Alert.alert('Status Error', e.message || 'Status check failed');
        } finally {
            setLoading(false);
        }
    }, [conceptId]);

    const handleStart = async () => {
        setLoading(true);
        setSubmitResult(null);
        setSelectedAnswers({});
        try {
            const data = await startQuestionnaire(conceptId);
            setQuestionnaire(data);
        } catch (e: any) {
            Alert.alert('Error', e.message || 'Failed to start questionnaire');
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
            Alert.alert('Submission Error', e.message || 'Submission failed');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadStatus();
    }, [loadStatus]);

    if (loading && !status && !questionnaire) {
        return (
            <View className="flex-1 items-center justify-center bg-canvas">
                <ActivityIndicator size="large" color="#38bdf8" />
                <Text className="mt-3 text-sm text-slate-400">Loading mastery status...</Text>
            </View>
        );
    }

    return (
        <ScrollView className="flex-1 bg-canvas p-5" contentContainerStyle={{ paddingBottom: 40 }}>
            {status && (
                <Card className="mb-5">
                    <View className="mb-2 flex-row items-center justify-between">
                        <Badge variant="accent">Mastery Tracking</Badge>
                        {status.is_mastered && (
                            <Badge variant="success">Fully Mastered</Badge>
                        )}
                    </View>
                    <CardTitle className="text-xl text-slate-50">{status.concept_name}</CardTitle>
                    <View className="mt-3 gap-2 border-t border-slate-800 pt-3">
                        <View className="flex-row items-center justify-between">
                            <Text className="text-xs text-slate-400">Current Tier Level</Text>
                            <Text className="text-sm font-bold text-sky-400">Tier {status.current_tier} / 5</Text>
                        </View>
                        <View className="flex-row items-center justify-between">
                            <Text className="text-xs text-slate-400">Eligible for Next Tier</Text>
                            <Text className={`text-xs font-bold ${status.eligibility?.eligible ? 'text-emerald-400' : 'text-amber-400'}`}>
                                {status.eligibility?.eligible ? 'YES' : 'LOCKED'}
                            </Text>
                        </View>
                        {!status.eligibility?.eligible && status.eligibility?.reason && (
                            <Text className="mt-1 text-xs text-amber-300/80 leading-relaxed">
                                {status.eligibility.reason}
                            </Text>
                        )}
                    </View>
                </Card>
            )}

            {!questionnaire && !submitResult && (
                <Button
                    variant="default"
                    onPress={handleStart}
                    className="py-4"
                >
                    <Award size={18} color="#020617" className="mr-2" />
                    Start Tier Questionnaire
                </Button>
            )}

            {questionnaire && (
                <View className="gap-4">
                    <View className="rounded-xl border border-sky-800 bg-sky-950/40 p-4">
                        <Text className="text-base font-bold text-sky-200">
                            Tier {questionnaire.tier} Test
                        </Text>
                        <Text className="mt-1 text-xs text-slate-400">
                            Pass criteria: {questionnaire.passing_threshold} / 10 correct answers
                        </Text>
                    </View>

                    {questionnaire.questions.map((q: any, qIdx: number) => (
                        <Card key={q.id}>
                            <Text className="mb-3 text-sm font-bold text-slate-100">
                                {qIdx + 1}. {q.prompt}
                            </Text>
                            <View className="gap-2">
                                {q.options.map((opt: string, optIdx: number) => {
                                    const isSelected = selectedAnswers[q.id] === optIdx;
                                    return (
                                        <TouchableOpacity
                                            key={optIdx}
                                            activeOpacity={0.8}
                                            onPress={() => setSelectedAnswers(prev => ({ ...prev, [q.id]: optIdx }))}
                                            className={`flex-row items-center rounded-xl border p-3.5 ${
                                                isSelected
                                                    ? 'border-sky-500 bg-sky-950/60'
                                                    : 'border-slate-800 bg-slate-900/60'
                                            }`}
                                        >
                                            <View
                                                className={`mr-3 h-6 w-6 items-center justify-center rounded-full border ${
                                                    isSelected
                                                        ? 'border-sky-400 bg-sky-500'
                                                        : 'border-slate-700 bg-slate-800'
                                                }`}
                                            >
                                                <Text
                                                    className={`text-xs font-bold ${
                                                        isSelected ? 'text-slate-950' : 'text-slate-400'
                                                    }`}
                                                >
                                                    {String.fromCharCode(65 + optIdx)}
                                                </Text>
                                            </View>
                                            <Text
                                                className={`flex-1 text-xs leading-relaxed ${
                                                    isSelected ? 'font-semibold text-sky-100' : 'text-slate-300'
                                                }`}
                                            >
                                                {opt}
                                            </Text>
                                        </TouchableOpacity>
                                    );
                                })}
                            </View>
                        </Card>
                    ))}

                    <Button
                        variant="default"
                        onPress={handleSubmit}
                        loading={loading}
                        className="py-4 mt-2"
                    >
                        Submit Questionnaire
                    </Button>
                </View>
            )}

            {submitResult && (
                <Card className={`mt-5 border ${submitResult.passed ? 'border-emerald-700 bg-emerald-950/30' : 'border-red-800 bg-red-950/30'}`}>
                    <View className="flex-row items-center gap-2 mb-2">
                        {submitResult.passed ? (
                            <CheckCircle2 size={22} color="#34d399" />
                        ) : (
                            <XCircle size={22} color="#f87171" />
                        )}
                        <CardTitle className="text-lg">
                            {submitResult.passed ? 'Tier Test Passed! 🎉' : 'Needs Review'}
                        </CardTitle>
                    </View>

                    <Text className="text-sm text-slate-300 mt-1">
                        Score: {submitResult.score} / {submitResult.total}
                    </Text>
                    <Text className="text-sm font-semibold text-sky-400 mt-1">
                        New Level: Tier {submitResult.new_tier}
                    </Text>

                    {submitResult.badge_awarded && (
                        <View className="mt-3 flex-row items-center gap-2 rounded-lg bg-amber-950/50 p-2.5 border border-amber-800">
                            <Award size={18} color="#fbbf24" />
                            <Text className="text-xs font-bold text-amber-200">
                                Concept Mastery Badge Awarded!
                            </Text>
                        </View>
                    )}

                    <Button
                        variant="secondary"
                        onPress={loadStatus}
                        className="mt-4"
                    >
                        Continue
                    </Button>
                </Card>
            )}
        </ScrollView>
    );
}