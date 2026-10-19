// DocumentPicker upload
// Sends multipart file and title. Redirects to ProcessingStatusScreen.
import React, { useState } from 'react';
import { View, Text, TextInput, Alert, Pressable } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import { uploadNote } from '@/api/notes';
import { ScreenHeader } from '@/components/ScreenHeader';

export default function UploadNoteScreen({ navigation }: any) {
    const [title, setTitle] = useState('');
    const [file, setFile] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const pickFile = async () => {
        const res = await DocumentPicker.getDocumentAsync({
            type: '*/*',
            copyToCacheDirectory: true,
        });
        if (!res.canceled && res.assets && res.assets.length > 0) {
            setFile(res.assets[0]);
        }
    };

    const handleUpload = async () => {
        if (!title.trim() || !file) {
            return Alert.alert('Validation', 'Please provide a title and pick a file.');
        }
        setLoading(true);
        try {
            const data = await uploadNote(title.trim(), file.uri, file.name, file.mimeType || 'text/plain');
            Alert.alert('Uploaded', `Note ID: ${data.id}`);
            navigation.navigate('ProcessingStatus', { noteId: data.id });
        } catch (error: any) {
            Alert.alert('Upload Error', JSON.stringify(error.response?.data || error.message));
        } finally {
            setLoading(false);
        }
    };

    return (
    <View className="flex-1 bg-canvas"><ScreenHeader title="Upload" navigation={navigation} /><View className="p-5">
      <Text className="mb-3 text-xl font-bold text-slate-50">Upload a note</Text>
      <TextInput
        placeholder="Note title" placeholderTextColor="#64748b"
        value={title}
        onChangeText={setTitle}
        className="mb-3 rounded-xl border border-slate-700 bg-slate-900 px-3 py-3 text-base text-slate-50"
      />
      <Pressable onPress={pickFile} className="items-center rounded-xl border border-slate-700 bg-slate-900 py-3"><Text className="font-semibold text-sky-300">{file ? file.name : 'Choose document'}</Text></Pressable>
      <View className="mt-3">
        <Pressable onPress={handleUpload} disabled={loading} className="items-center rounded-xl bg-sky-500 py-3 disabled:opacity-50"><Text className="font-bold text-slate-950">{loading ? 'Uploading…' : 'Submit note'}</Text></Pressable>
      </View>
    </View></View>
  );
}
