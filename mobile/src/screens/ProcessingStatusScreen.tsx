// Polls UPLOADED -> VERIFIED
/*Polls every 2 seconds. Visual steps: uploaded →→ ocr_done →→ claims_extracted →→ verified.*/

import React, { useEffect, useRef, useState } from 'react';
import { View, Text, Button } from 'react-native';
import { getNoteStatus } from '@/api/notes';

export default function ProcessingStatusScreen({ route, navigation }: any) {
    const { noteId } = route.params || { noteId: 1 };
    const [note, setNote] = useState<any>(null);
    const [accessDenied, setAccessDenied] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const deniedRef = useRef(false);

    const fetchStatus = async () => {
        if (deniedRef.current) return;
        try {
            const data = await getNoteStatus(noteId);
            setNote(data);
        } catch (error: any) {
            if (error.response?.status === 403) {
                deniedRef.current = true;
                setAccessDenied(true);
                setError(error.response?.data?.detail || null);
                return;
            }
            setError(error.response?.data?.detail || error.message || 'Could not load note status.');
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
      {accessDenied ? (
        <Text style={{ marginVertical: 12 }}>
          {error || 'Your account cannot access this note. Check that you are signed in with the account that uploaded it.'}
        </Text>
      ) : null}
      {error ? <Text style={{ color: 'red', marginVertical: 10 }}>{error}</Text> : null}
      {!accessDenied ? <>
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
      </> : null}
    </View>
  );
}
