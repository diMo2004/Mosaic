// Mandatory onboarding modal
// Submits full_name, education_level, learning_goal. Unlocks IsProfileComplete guard.
// Backend Endpoint: POST /api/auth/complete-profile/

import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, Alert, Pressable } from 'react-native';
import { completeProfile, getProfile } from '@/api/auth';

export default function CompleteProfileScreen({ navigation, route }: any) {
    const [fullName, setFullName] = useState('');
    const [educationLevel, setEducationLevel] = useState('');
    const [learningGoal, setLearningGoal] = useState('');
    const [interests, setInterests] = useState('');
    const [profileLoaded, setProfileLoaded] = useState(false);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        const initialProfile = route?.params?.profile;
        if (initialProfile) {
            setFullName(initialProfile.full_name || '');
            setEducationLevel(initialProfile.education_level || '');
            setLearningGoal(initialProfile.learning_goal || '');
            setInterests(Array.isArray(initialProfile.interests) ? initialProfile.interests.join(', ') : '');
            setProfileLoaded(true);
            return;
        }

        getProfile().then((profile) => {
            setFullName(profile.full_name || '');
            setEducationLevel(profile.education_level || '');
            setLearningGoal(profile.learning_goal || '');
            setInterests(Array.isArray(profile.interests) ? profile.interests.join(', ') : '');
        }).catch((error: any) => {
            Alert.alert('Profile Error', error.response?.data?.detail || error.message);
        }).finally(() => setProfileLoaded(true));
    }, []);

    const handleComplete = async () => {
        const normalizedName = fullName.trim();
        const normalizedEducation = educationLevel.trim();
        const normalizedGoal = learningGoal.trim();
        if (!normalizedName || !normalizedEducation || !normalizedGoal) {
            Alert.alert('Required fields', 'Enter your full name, education level, and learning goal.');
            return;
        }

        setSaving(true);
        try {
            const result = await completeProfile({
                full_name: normalizedName,
                education_level: normalizedEducation,
                learning_goal: normalizedGoal,
                interests: interests.split(',').map((interest) => interest.trim()).filter(Boolean),
            });
            if (result.profile_completed && route?.name === 'CompleteProfile') {
                navigation.reset({ index: 0, routes: [{ name: 'Main' }] });
            } else {
                Alert.alert('Success', 'Profile saved successfully.');
            }
        } catch (error: any) {
            const detail = error.response?.data?.detail
                || Object.entries(error.response?.data || {})
                    .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
                    .join('\n')
                || error.message
                || 'Please try again.';
            Alert.alert('Could not save profile', detail);
        } finally {
            setSaving(false);
        }
    };

    return (
    <View className="flex-1 bg-canvas p-5 pt-10">
      <Text className="mb-2 text-2xl font-bold text-slate-50">Your profile</Text>
      <Text className="mb-6 text-slate-400">Use these preferences to tailor your learning experience.</Text>
      <TextInput
        placeholder="Full name" placeholderTextColor="#64748b"
        value={fullName}
        onChangeText={setFullName}
        className="mb-3 rounded-xl border border-slate-700 bg-slate-900 px-3 py-3 text-slate-50"
      />
      <TextInput
        placeholder="Education level" placeholderTextColor="#64748b"
        value={educationLevel}
        onChangeText={setEducationLevel}
        className="mb-3 rounded-xl border border-slate-700 bg-slate-900 px-3 py-3 text-slate-50"
      />
      <TextInput
        placeholder="Learning goal" placeholderTextColor="#64748b"
        value={learningGoal}
        onChangeText={setLearningGoal}
        className="mb-3 rounded-xl border border-slate-700 bg-slate-900 px-3 py-3 text-slate-50"
      />
      <TextInput
        placeholder="Interests, comma separated" placeholderTextColor="#64748b"
        value={interests}
        onChangeText={setInterests}
        className="mb-5 rounded-xl border border-slate-700 bg-slate-900 px-3 py-3 text-slate-50"
      />
      <Pressable onPress={handleComplete} disabled={!profileLoaded || saving} className="items-center rounded-xl bg-sky-500 py-3 disabled:opacity-50"><Text className="font-bold text-slate-950">{!profileLoaded ? 'Loading profile…' : saving ? 'Saving profile…' : 'Save profile & continue'}</Text></Pressable>
    </View>
  );
}
