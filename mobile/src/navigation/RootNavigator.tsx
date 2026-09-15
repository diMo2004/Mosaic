// Auth stack vs App tabs (Feed, Upload, Playlists)
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

import LoginScreen from '@/screens/LoginScreen';
import FeedScreen from '@/screens/FeedScreen';
import CompleteProfileScreen from '@/screens/CompleteProfileScreen';
import FlashcardDetailScreen from '@/screens/FlashcardDetailScreen';
import UploadNoteScreen from '@/screens/UploadNoteScreen';
import ProcessingStatusScreen from '@/screens/ProcessingStatusScreen';
import ClaimReviewScreen from '@/screens/ClaimReviewScreen';
import PlaylistModal from '@/screens/PlaylistModal';
import GroundedExplainScreen from '@/screens/GroundedExplainScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function MainTabs() {
    return (
    <Tab.Navigator>
      <Tab.Screen name="Feed" component={FeedScreen} />
      <Tab.Screen name="Upload" component={UploadNoteScreen} />
      <Tab.Screen name="Playlists" component={PlaylistModal} />
      <Tab.Screen name="Profile" component={CompleteProfileScreen} />
    </Tab.Navigator>
    )
}

export default function RootNavigator() {
  return (
    <Stack.Navigator initialRouteName="Login">
      <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
      <Stack.Screen name="CompleteProfile" component={CompleteProfileScreen} />
      <Stack.Screen name="Main" component={MainTabs} options={{ headerShown: false }} />
      <Stack.Screen name="FlashcardDetail" component={FlashcardDetailScreen} />
      <Stack.Screen name="ProcessingStatus" component={ProcessingStatusScreen} />
      <Stack.Screen name="ClaimReview" component={ClaimReviewScreen} />
      <Stack.Screen name="PlaylistModal" component={PlaylistModal} options={{ presentation: 'modal' }} />
      <Stack.Screen name="GroundedExplain" component={GroundedExplainScreen} />
    </Stack.Navigator>
  );
}