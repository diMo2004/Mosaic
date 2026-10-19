import React from 'react';
import { Text, View } from 'react-native';
import { ProfileMenu } from './ProfileMenu';

export function ScreenHeader({ title, navigation }: { title: string; navigation: any }) {
  return (
    <View className="flex-row items-center justify-between border-b border-slate-800 bg-canvas px-5 py-3">
      <Text className="text-2xl font-bold text-slate-50">{title}</Text>
      <ProfileMenu navigation={navigation} />
    </View>
  );
}
