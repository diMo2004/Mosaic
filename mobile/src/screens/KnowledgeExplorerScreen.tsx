// Location: mobile/src/screens/KnowledgeExplorerScreen.tsx
import React, { useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, ActivityIndicator, Pressable } from 'react-native';
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
        <View className="flex-1 bg-canvas p-5">
            <View className="mb-4 flex-row gap-2">
                {(['claims', 'sources', 'evidence'] as const).map(tab => <Pressable key={tab} onPress={() => fetchTab(tab)} className={`rounded-lg px-3 py-2 ${activeTab === tab ? 'bg-sky-500' : 'bg-slate-800'}`}><Text className={activeTab === tab ? 'font-bold text-slate-950' : 'font-bold text-slate-300'}>{tab[0].toUpperCase() + tab.slice(1)}</Text></Pressable>)}
            </View>

            {loading ? <ActivityIndicator size="large" color="#38bdf8" /> : (
                <FlatList
                    data={data}
                    keyExtractor={(item) => item.id.toString()}
                    renderItem={({ item }) => (
                        <View className="border-b border-slate-800 py-3">
                            {activeTab === 'claims' && (
                                <TouchableOpacity onPress={() => navigation.navigate('GroundedExplain', { canonicalClaimId: item.id })}>
                                    <Text className="font-semibold text-slate-100">{item.text}</Text>
                                    <Text className="mt-1 text-sky-300">Tap for grounded explanation</Text>
                                </TouchableOpacity>
                            )}
                            {activeTab === 'sources' && (
                                <Text className="text-slate-200">{item.name} ({item.source_type})</Text>
                            )}
                            {activeTab === 'evidence' && (
                                <Text className="text-slate-200">{item.title} · {item.relation}</Text>
                            )}
                        </View>
                    )}
                    ListEmptyComponent={<Text className="mt-5 text-center text-slate-400">No {activeTab} found.</Text>}
                />
            )}
        </View>
    );
}
