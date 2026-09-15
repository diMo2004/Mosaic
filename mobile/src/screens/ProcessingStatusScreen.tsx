// Polls UPLOADED -> VERIFIED
/*Polls every 2 seconds. Visual steps: uploaded →→ ocr_done →→ claims_extracted →→ verified.*/

import React, { useEffect, useState } from 'react';
import { View, Text, Button, Alert } from 'react-native';
import { getNoteStatus } from '@/api/notes';

export default function ProcessingStatusScreen({ route, navigation }: any) {
    const { noteId } = route.params || { noteId: 1 };
    const [note, setNote] = useState<any>(null);

    const fetchStatus = async () => {
        try {
            const data = await getNoteStatus(noteId);
            setNote(data);
        } catch (error: any) {
            Alert.alert('Status Error', JSON.stringify(error.response?.data || error.message));
        }
    };
    
    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 3000);
        return () => clearInterval(interval);
    }, [noteId]);

    return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Processing Status (Note #{noteId})</Text>
      <Text style={{ marginVertical: 10, fontSize: 16 }}>
        Status: <Text style={{ fontWeight: 'bold' }}>{note?.status || 'Loading...'}</Text>
      </Text>
      {note?.processing_error ? (
        <Text style={{ color: 'red', marginBottom: 10 }}>Error: {note.processing_error}</Text>
      ) : null}
      <Text numberOfLines={6} style={{ backgroundColor: '#eee', padding: 8, marginVertical: 10 }}>
        {note?.extracted_text || 'No text extracted yet...'}
      </Text>
      <Button title="Refresh Status" onPress={fetchStatus} />
      <View style={{ marginTop: 10 }}>
        <Button title="View Claims" onPress={() => navigation.navigate('ClaimReview')} />
      </View>
    </View>
  );
}