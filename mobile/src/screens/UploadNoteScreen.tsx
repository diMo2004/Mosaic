// DocumentPicker upload
// Sends multipart file and title. Redirects to ProcessingStatusScreen.
import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import { uploadNote } from '@/api/notes';

export default function UploadNoteScreen({ navigation }: any) {
    const [title, setTitle] = useState('');
    const [file, setFile] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const pickFile = async () => {
        const res = await DocumentPicker.getDocumentAsync({ type: '*/*' });
        if (!res.canceled && res.assets && res.assets.length > 0) {
            setFile(res.assets[0]);
        }
    };

    const handleUpload = async () => {
        if (!title || !file) {
            return Alert.alert('Validation', 'Please provide a title and pick a file.');
        }
        setLoading(true);
        try {
            const data = await uploadNote(title, file.uri, file.name, file.mimeType || 'text/plain');
            Alert.alert('Uploaded', 'Note ID: ${data.id}');
            navigation.navigate('ProcessingStatus', { noteId: data.id });
        } catch (error: any) {
            Alert.alert('Upload Error', JSON.stringify(error.response?.data || error.message));
        } finally {
            setLoading(false);
        }
    };

    return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold', marginBottom: 10 }}>Upload Note</Text>
      <TextInput
        placeholder="Note Title"
        value={title}
        onChangeText={setTitle}
        style={{ borderWidth: 1, padding: 8, marginBottom: 10 }}
      />
      <Button title={file ? `File: ${file.name}` : 'Pick Document'} onPress={pickFile} />
      <View style={{ marginTop: 15 }}>
        <Button title={loading ? 'Uploading...' : 'Submit Note'} onPress={handleUpload} disabled={loading} />
      </View>
    </View>
  );
}