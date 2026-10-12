// Location: mobile/src/screens/KnowledgeExplorerScreen.tsx
import React, { useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, Button, ActivityIndicator } from 'react-native';
import { getSources, getCanonicalClaims, getEvidenceList } from '../api/knowledge';

export default function KnowledgeExplorerScreen({ navigation }: any) {
    const [activeTab, setActiveTab] = useState<'claims' | 'sources' | 'evidence'>('claims');
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    const fetchTab = async (tab: 'claims' | 'sources' | 'evidence') => {
        setActiveTab(tab);
        setLoading(true);
        try {
            let res = [];
            if (tab === 'claims') res = await getCanonicalClaims();
            else if (tab === 'sources') res = await getSources();
            else if (tab === 'evidence') res = await getEvidenceList();
            setData(Array.isArray(res) ? res : res.results || []);
        } catch (err: any) {
            alert(err.message || 'Fetch error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <View style={{ flex: 1, padding: 16 }}>
            <View style={{ flexDirection: 'row', justifyContent: 'space-around', marginBottom: 16 }}>
                <Button title="Claims" onPress={() => fetchTab('claims')} color={activeTab === 'claims' ? 'blue' : 'gray'} />
                <Button title="Sources" onPress={() => fetchTab('sources')} color={activeTab === 'sources' ? 'blue' : 'gray'} />
                <Button title="Evidence" onPress={() => fetchTab('evidence')} color={activeTab === 'evidence' ? 'blue' : 'gray'} />
            </View>

            {loading ? <ActivityIndicator size="large" /> : (
                <FlatList
                    data={data}
                    keyExtractor={(item) => item.id.toString()}
                    renderItem={({ item }) => (
                        <View style={{ padding: 10, borderBottomWidth: 1, borderColor: '#eee' }}>
                            {activeTab === 'claims' && (
                                <TouchableOpacity onPress={() => navigation.navigate('GroundedExplain', { canonicalClaimId: item.id })}>
                                    <Text style={{ fontWeight: 'bold' }}>Claim #{item.id}: {item.text}</Text>
                                    <Text style={{ color: 'blue' }}>Tap to view RAG Grounded Explain</Text>
                                </TouchableOpacity>
                            )}
                            {activeTab === 'sources' && (
                                <Text>Source #{item.id}: {item.name} ({item.source_type})</Text>
                            )}
                            {activeTab === 'evidence' && (
                                <Text>Evidence #{item.id}: {item.title} - {item.relation}</Text>
                            )}
                        </View>
                    )}
                    ListEmptyComponent={<Text style={{ textAlign: 'center', marginTop: 20 }}>Select a tab or empty.</Text>}
                />
            )}
        </View>
    );
}