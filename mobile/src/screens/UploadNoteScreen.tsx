// DocumentPicker upload
// Sends multipart file and title. Redirects to ProcessingStatusScreen.
import React, { useState } from 'react';
import { View, Text, TextInput, Pressable } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import { uploadNote } from '@/api/notes';
import { ScreenHeader } from '@/components/ScreenHeader';
import { apiErrorMessage, notify } from '@/utils/notify';

const ACCEPTED_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'image/jpeg',
    'image/png',
    'image/webp',
    'text/plain',
];
const MAX_BYTES = 10 * 1024 * 1024;

export default function UploadNoteScreen({ navigation }: any) {
    const [title, setTitle] = useState('');
    const [file, setFile] = useState<DocumentPicker.DocumentPickerAsset | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const pickFile = async () => {
        setError(null);
        const res = await DocumentPicker.getDocumentAsync({
            type: ACCEPTED_TYPES,
            copyToCacheDirectory: true,
        });
        if (res.canceled || !res.assets?.length) return;
        const asset = res.assets[0];
        if (asset.size && asset.size > MAX_BYTES) {
            setError('That file is larger than 10 MB. Pick a smaller file.');
            return;
        }
        setFile(asset);
        if (!title.trim()) setTitle(asset.name.replace(/\.[^.]+$/, ''));
    };

    const handleUpload = async () => {
        if (!title.trim() || !file) {
            setError('Add a title and choose a file first.');
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const data = await uploadNote(title.trim(), {
                uri: file.uri,
                name: file.name,
                mimeType: file.mimeType,
                file: (file as any).file ?? null,
            });
            setFile(null);
            setTitle('');
            navigation.navigate('ProcessingStatus', { noteId: data.id });
        } catch (err: any) {
            const message = apiErrorMessage(err, 'Upload failed. Please try again.');
            setError(message);
            notify('Upload failed', message);
        } finally {
            setLoading(false);
        }
    };

    return (
    <View className="flex-1 bg-canvas"><ScreenHeader title="Upload" navigation={navigation} /><View className="p-5">
      <Text className="mb-1 text-xl font-bold text-slate-50">Upload a note</Text>
      <Text className="mb-4 text-sm text-slate-400">PDF, Word, PowerPoint, image, or .txt, up to 10 MB. Verified facts from it become personal flashcards.</Text>
      <TextInput
        placeholder="Note title" placeholderTextColor="#64748b"
        value={title}
        onChangeText={setTitle}
        className="mb-3 rounded-xl border border-slate-700 bg-slate-900 px-3 py-3 text-base text-slate-50"
      />
      <Pressable onPress={pickFile} className="items-center rounded-xl border border-slate-700 bg-slate-900 py-3"><Text className="font-semibold text-sky-300">{file ? file.name : 'Choose document'}</Text></Pressable>
      {error ? <Text className="mt-3 text-red-300">{error}</Text> : null}
      <View className="mt-3">
        <Pressable onPress={handleUpload} disabled={loading} className="items-center rounded-xl bg-sky-500 py-3 disabled:opacity-50"><Text className="font-bold text-slate-950">{loading ? 'Uploading and processing…' : 'Submit note'}</Text></Pressable>
      </View>
    </View></View>
  );
}
