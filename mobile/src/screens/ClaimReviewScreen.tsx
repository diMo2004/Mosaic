// Review extracted claims
import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Button, Alert } from 'react-native';
import { getExtractedClaims, verifyClaim } from '@/api/notes';

export default function ClaimReviewScreen() {
    const [claims, setClaims] = useState<any[]>([]);

    const loadClaims = async () => {
        try {
            const data = await getExtractedClaims();
            setClaims(data.results || data);
        } catch (err: any) {
            Alert.alert('Error', JSON.stringify(err.response?.data || err.message));
        }
    };

    useEffect(() => {
        loadClaims();
    }, []);

    const handleVerify = async (id: number) => {
        try {
            const res = await verifyClaim(id);
            Alert.alert('Verification Result', `Status: ${res.status}\nConfidence: ${res.confidence}`);
            loadClaims(); // Refresh claims after verification
        } catch (error: any) {
            Alert.alert('Verification Error', JSON.stringify(error.response?.data || error.message));
        }
    };
    
    return (
    <View style={{ padding: 20, flex: 1 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold', marginBottom: 10 }}>Extracted Claims</Text>
      <Button title="Refresh Claims" onPress={loadClaims} />
      <FlatList
        data={claims}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <View style={{ padding: 10, borderBottomWidth: 1, borderColor: '#ccc' }}>
            <Text style={{ fontWeight: 'bold' }}>#{item.id}: {item.text}</Text>
            <Text>Status: {item.status} | Confidence: {item.confidence}</Text>
            <Button title="Run Verification" onPress={() => handleVerify(item.id)} />
          </View>
        )}
      />
    </View>
  );
}