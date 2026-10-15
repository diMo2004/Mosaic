// Mandatory onboarding modal
// Submits full_name, education_level, learning_goal. Unlocks IsProfileComplete guard.
// Backend Endpoint: POST /api/auth/complete-profile/

import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
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
    <View style={{ padding: 20, marginTop: 40 }}>
      <Text style={{ fontSize: 20, fontWeight: 'bold', marginBottom: 20 }}>
        Mandatory Profile Onboarding
      </Text>
      <TextInput
        placeholder="Full Name"
        value={fullName}
        onChangeText={setFullName}
        style={{ borderWidth: 1, padding: 8, marginBottom: 10 }}
      />
      <TextInput
        placeholder="Education Level"
        value={educationLevel}
        onChangeText={setEducationLevel}
        style={{ borderWidth: 1, padding: 8, marginBottom: 10 }}
      />
      <TextInput
        placeholder="Learning Goal"
        value={learningGoal}
        onChangeText={setLearningGoal}
        style={{ borderWidth: 1, padding: 8, marginBottom: 10 }}
      />
      <TextInput
        placeholder="Interests (comma separated)"
        value={interests}
        onChangeText={setInterests}
        style={{ borderWidth: 1, padding: 8, marginBottom: 20 }}
      />
      <Button
        title={!profileLoaded ? 'Loading Profile...' : saving ? 'Saving Profile...' : 'Save Profile & Continue'}
        onPress={handleComplete}
        disabled={!profileLoaded || saving}
      />
    </View>
  );
}
