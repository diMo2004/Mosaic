// Login & Register
// Stores access and refresh in SecureStore. If response has status: "profile_required", navigates immediately to CompleteProfile.
import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, ActivityIndicator} from 'react-native';
import { login, register } from '@/api/auth';

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
        await register(username, email, password);
        Alert.alert('Registration successful', 'You can now log in with your credentials.');
      }
      await login(username, password);
      navigation.replace('Main');
    } catch (error: any) {
        Alert.alert('Error', JSON.stringify(error.response?.data || error.message));
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
      <View style={{ marginTop: 12 }}>
        <Button
          title="Skip to Complete Profile"
          onPress={() => navigation.navigate('CompleteProfile')}
          color="#888"
        />
      </View>
    </View>
  );
}