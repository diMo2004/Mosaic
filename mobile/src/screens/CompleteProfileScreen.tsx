// Mandatory onboarding modal
// Submits full_name, education_level, learning_goal. Unlocks IsProfileComplete guard.
// Backend Endpoint: POST /api/auth/complete-profile/

import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import { completeProfile } from '@/api/auth';

export default function CompleteProfileScreen({ navigation }: any) {
    const [fullName, setFullName] = useState('');
    const [educationLevel, setEducationLevel] = useState('Undergraduate');
    const [learningGoal, setLearningGoal] = useState('Gate CSE Preparation');
    const [interests, setInterests] = useState('Algorithms, Operating Systems');

    const handleComplete = async () => {
        try {
            await completeProfile({
                full_name: fullName,
                education_level: educationLevel,
                learning_goal: learningGoal,
                interests: interests.split(',').map((interest) => interest.trim()),
            });
            Alert.alert('Success', 'Profile completed successfully.');
            navigation.replace('Main');
        } catch (error: any) {
            Alert.alert('Error', JSON.stringify(error.response?.data || error.message));
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
      <Button title="Save Profile & Continue" onPress={handleComplete} />
    </View>
  );
}