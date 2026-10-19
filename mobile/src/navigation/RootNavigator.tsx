// Auth stack vs App tabs (Feed, Upload, Playlists)
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Home, Search, Upload } from 'lucide-react-native';

import LoginScreen from '@/screens/LoginScreen';
import FeedScreen from '@/screens/FeedScreen';
import CompleteProfileScreen from '@/screens/CompleteProfileScreen';
import FlashcardDetailScreen from '@/screens/FlashcardDetailScreen';
import UploadNoteScreen from '@/screens/UploadNoteScreen';
import ProcessingStatusScreen from '@/screens/ProcessingStatusScreen';
import ClaimReviewScreen from '@/screens/ClaimReviewScreen';
import PlaylistModal from '@/screens/PlaylistModal';
import GroundedExplainScreen from '@/screens/GroundedExplainScreen';
import NotesListScreen from '@/screens/NotesListScreen';
import KnowledgeExplorerScreen from '@/screens/KnowledgeExplorerScreen';
import ProgressScreen from '@/screens/ProgressScreen';
import MasteryScreen from '@/screens/MasteryScreen';
import SearchScreen from '@/screens/SearchScreen';
import PlaylistDetailScreen from '@/screens/PlaylistDetailScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function MainTabs() {
    return (
        <Tab.Navigator screenOptions={({ route }) => ({ headerShown: false, tabBarStyle: { backgroundColor: '#0f172a', borderTopColor: '#1e293b' }, tabBarActiveTintColor: '#38bdf8', tabBarInactiveTintColor: '#94a3b8', tabBarIcon: ({ color, size }) => route.name === 'Feed' ? <Home color={color} size={size} /> : route.name === 'Upload' ? <Upload color={color} size={size} /> : <Search color={color} size={size} /> })}>
            <Tab.Screen name="Feed" component={FeedScreen} />
            <Tab.Screen name="Upload" component={UploadNoteScreen} />
            <Tab.Screen name="Search" component={SearchScreen} />
        </Tab.Navigator>
    );
}

export default function RootNavigator() {
    return (
        <Stack.Navigator initialRouteName="Login" screenOptions={{ headerStyle: { backgroundColor: '#090d16' }, headerTintColor: '#f8fafc', contentStyle: { backgroundColor: '#090d16' } }}>
            <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
            <Stack.Screen name="CompleteProfile" component={CompleteProfileScreen} />
            <Stack.Screen name="Main" component={MainTabs} options={{ headerShown: false }} />
            <Stack.Screen name="FlashcardDetail" component={FlashcardDetailScreen} />
            <Stack.Screen name="ProcessingStatus" component={ProcessingStatusScreen} />
            <Stack.Screen name="ClaimReview" component={ClaimReviewScreen} />
            <Stack.Screen name="PlaylistModal" component={PlaylistModal} options={{ presentation: 'modal' }} />
            <Stack.Screen name="GroundedExplain" component={GroundedExplainScreen} />
            <Stack.Screen name="Mastery" component={MasteryScreen} />
            <Stack.Screen name="Notes" component={NotesListScreen} />
            <Stack.Screen name="Knowledge" component={KnowledgeExplorerScreen} />
            <Stack.Screen name="Progress" component={ProgressScreen} />
            <Stack.Screen name="Playlists" component={PlaylistModal} />
            <Stack.Screen name="PlaylistDetail" component={PlaylistDetailScreen} options={{ title: 'Playlist' }} />
        </Stack.Navigator>
    );
}
