import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { DarkTheme, NavigationContainer } from '@react-navigation/native';
import RootNavigator from './src/navigation/RootNavigator';
import './global.css';

export default function App() {
  const theme = { ...DarkTheme, colors: { ...DarkTheme.colors, primary: '#38bdf8', background: '#090d16', card: '#0f172a', text: '#f8fafc', border: '#1e293b', notification: '#38bdf8' } };
  return (
    <NavigationContainer theme={theme}>
      <RootNavigator />
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
