import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, Button, ActivityIndicator } from 'react-native';
import { getNotes } from '../api/notes';

export default function NotesListScreen({ navigation }: any) {
    const [notes, setNotes] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const load = async () => {
        setLoading(true);
        try {
            const data = await getNotes();
            setNotes(Array.isArray(data) ? data : data.results || []);
        } catch (err: any) {
            alert(err.message || 'Failed to fetch notes');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        load();
    }, []);

    return (
        <View style={{ flex: 1, padding: 16 }}>
            <Button title="Refresh Notes" onPress={load} />
            {loading ? <ActivityIndicator size="large" style={{ marginTop: 20 }} /> : (
                <FlatList
                    data={notes}
                    keyExtractor={(item) => item.id.toString()}
                    renderItem={({ item }) => (
                        <TouchableOpacity
                            onPress={() => navigation.navigate('ProcessingStatus', { noteId: item.id })}
                            style={{ padding: 12, borderBottomWidth: 1, borderColor: '#ccc' }}
                        >
                            <Text style={{ fontWeight: 'bold' }}>ID {item.id}: {item.title || 'Untitled'}</Text>
                            <Text>Status: {item.status}</Text>
                        </TouchableOpacity>
                    )}
                    ListEmptyComponent={<Text style={{ marginTop: 20, textAlign: 'center' }}>No notes found.</Text>}
                />
            )}
        </View>
    );
} 