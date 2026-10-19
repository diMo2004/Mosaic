// Login & Register
// Stores access and refresh in SecureStore. If response has status: "profile_required", navigates immediately to CompleteProfile.
import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, ActivityIndicator} from 'react-native';
import axios from 'axios';
import { login, register } from '@/api/auth';

function getAuthErrorMessage(error: unknown): string {
  if (!axios.isAxiosError(error)) {
    return error instanceof Error ? error.message : 'Login failed. Please try again.';
  }

  if (error.code === 'ECONNABORTED' || error.code === 'ETIMEDOUT') {
    return 'The local backend did not respond within 30 seconds. Check that the local tunnel and Django server are running, then try again.';
  }
  if (!error.response) {
    return 'Could not reach the local backend. Restart the local tunnel launcher and confirm this app is using the current Expo session.';
  }
  if (error.response.status === 401) {
    return 'The username or password is incorrect.';
  }
  if (error.response.status === 503) {
    return 'The local backend is running but cannot reach the Neon database. Check the backend terminal and DATABASE_URL.';
  }

  const data = error.response.data as { detail?: unknown } | string | undefined;
  if (typeof data === 'string' && /<!doctype|<html/i.test(data)) {
    return `The backend returned an HTML error (${error.response.status}). Check the Django terminal for the server-side cause.`;
  }
  if (data && typeof data === 'object' && typeof data.detail === 'string') {
    return data.detail;
  }
  return typeof data === 'string' ? data : `Login failed with status ${error.response.status}.`;
}

export default function LoginScreen({navigation}: any) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if(!username || !password || (isRegister && !email)) {
      return Alert.alert('Validation', 'Please fill in all required fields.');
    }
    setLoading(true);
    try {
      if (isRegister) {
        const result = await register(username.trim(), email.trim(), password);
        navigation.replace(result.profile_completed ? 'Main' : 'CompleteProfile', {
          profile: result.profile,
        });
        return;
      }
      const result = await login(username.trim(), password);
      navigation.replace(result.profile_completed ? 'Main' : 'CompleteProfile', {
        profile: result.profile,
      });
    } catch (error: unknown) {
        Alert.alert('Login Error', getAuthErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const inputStyle = {
    borderWidth: 1,
    borderColor: '#333',
    backgroundColor: '#ffffff',
    color: '#000000',
    padding: 10,
    marginBottom: 12,
    borderRadius: 6,
    fontSize: 16,
  };

  return (
    <View style={{ flex: 1, backgroundColor: '#f8f9fa', padding: 24, justifyContent: 'center' }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#111', marginBottom: 24, textAlign: 'center' }}>
        {isRegister ? 'Create Account' : 'Mosaic Login'}
      </Text>
      <TextInput
        placeholder="Username"
        placeholderTextColor="#888"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
        style={inputStyle}
      />
      {isRegister && (
        <TextInput
          placeholder="Email address"
          placeholderTextColor="#888"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
          style={inputStyle}
        />
      )}
      <TextInput
        placeholder="Password"
        placeholderTextColor="#888"
        value={password}
        secureTextEntry
        onChangeText={setPassword}
        style={inputStyle}
      />
      {loading ? (
        <ActivityIndicator size="large" color="#0066cc" style={{ marginVertical: 10 }} />
      ) : (
        <Button
          title={isRegister ? 'Register & Log In' : 'Log In'}
          onPress={handleSubmit}
          color="#0066cc"
        />
      )}
      <View style={{ marginTop: 16 }}>
        <Button
          title={isRegister ? 'Already have an account? Log In' : 'Need an account? Register'}
          onPress={() => setIsRegister(!isRegister)}
          color="#555"
        />
      </View>
    </View>
  );
}
