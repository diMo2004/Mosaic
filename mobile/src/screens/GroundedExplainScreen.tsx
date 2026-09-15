// in-depth evidence citations
// Renders explanation paragraph + expandable evidence citation cards with source authority scores.
// GET /api/learning/canonical-claims/{id}/explain/

import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, ScrollView } from 'react-native';
import {getExplanation} from '@/api/learning';

export default function GroundedExplainScreen({ route }: any) {
    const { claimId } = route.params;
    const [data, setData] = useState<any>(null);

    useEffect(() => {
        getExplanation(claimId).then(setData).catch(console.error);
    }, [claimId]);

    if (!data) return <Text style={{ padding: 20 }}>Loading explanation...</Text>;

    return (
    <ScrollView style={{ padding: 20 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Grounded Explanation</Text>
      <Text style={{ fontStyle: 'italic', marginVertical: 8 }}>Claim: {data.canonical_claim?.text}</Text>
      <Text style={{ backgroundColor: '#eef', padding: 10, marginVertical: 10 }}>{data.explanation}</Text>
      <Text style={{ fontSize: 16, fontWeight: 'bold', marginTop: 15 }}>Evidence Provenance:</Text>
      {data.evidence?.map((item: any, idx: number) => (
        <View key={idx} style={{ borderWidth: 1, padding: 8, marginVertical: 6 }}>
          <Text style={{ fontWeight: 'bold' }}>Source: {item.source}</Text>
          <Text>Relation: {item.relation} | Relevance: {item.relevance_score}</Text>
          <Text style={{ color: '#555', marginTop: 4 }}>"{item.excerpt}"</Text>
        </View>
      ))}
    </ScrollView>
    );
}