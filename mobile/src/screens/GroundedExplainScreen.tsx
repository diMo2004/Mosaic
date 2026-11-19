// in-depth evidence citations
// GET /api/learning/canonical-claims/{id}/explain/

import React, { useEffect, useState } from 'react';
import { ActivityIndicator, ScrollView, Text, View } from 'react-native';
import { getExplanation } from '@/api/learning';

export default function GroundedExplainScreen({ route }: any) {
    const claimId = route?.params?.claimId;
    const [data, setData] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!claimId) {
            setError('This card has no canonical claim to explain.');
            return;
        }
        let cancelled = false;
        getExplanation(claimId)
            .then((explanation) => {
                if (!cancelled) setData(explanation);
            })
            .catch((err: any) => {
                if (!cancelled) {
                    setError(err.response?.data?.detail || err.message || 'Could not load the explanation.');
                }
            });
        return () => {
            cancelled = true;
        };
    }, [claimId]);

    if (error) {
        return (
            <View className="flex-1 bg-canvas p-5">
                <Text className="text-xl font-bold text-slate-50">Grounded explanation</Text>
                <Text className="mt-4 text-red-300">{error}</Text>
            </View>
        );
    }

    if (!data) {
        return (
            <View className="flex-1 items-center justify-center bg-canvas">
                <ActivityIndicator color="#38bdf8" />
                <Text className="mt-3 text-slate-300">Loading explanation...</Text>
            </View>
        );
    }

    return (
        <ScrollView className="flex-1 bg-canvas p-5">
            <Text className="text-xl font-bold text-slate-50">Grounded explanation</Text>
            <Text className="mt-3 italic text-slate-300">Claim: {data.canonical_claim?.text}</Text>
            <Text className="mt-4 rounded-xl bg-slate-900 p-3 text-slate-100">{data.explanation}</Text>
            <Text className="mt-5 text-base font-bold text-slate-50">Evidence</Text>
            {(data.evidence || []).length === 0 ? (
                <Text className="mt-2 text-slate-400">No evidence citations were returned.</Text>
            ) : null}
            {data.evidence?.map((item: any, idx: number) => (
                <View key={idx} className="mt-3 rounded-xl border border-slate-800 p-3">
                    <Text className="font-semibold text-slate-100">Source: {item.source}</Text>
                    <Text className="mt-1 text-slate-400">Relation: {item.relation} | Relevance: {item.relevance_score}</Text>
                    <Text className="mt-2 text-slate-300">"{item.excerpt}"</Text>
                </View>
            ))}
        </ScrollView>
    );
}
