import React, { useState } from 'react';
import { Modal, Pressable, Text, TouchableWithoutFeedback, View } from 'react-native';
import { BookOpen, ChartColumn, FileText, ListMusic, UserRound } from 'lucide-react-native';

const destinations = [
  ['Notes', FileText],
  ['Progress', ChartColumn],
  ['Playlists', ListMusic],
  ['Knowledge', BookOpen],
] as const;

export function ProfileMenu({ navigation }: { navigation: any }) {
  const [open, setOpen] = useState(false);
  const rootNavigation = navigation.getParent?.() ?? navigation;

  return (
    <View className="relative">
      <Pressable
        accessibilityRole="button"
        accessibilityLabel="Open profile menu"
        onPress={() => setOpen(true)}
        className="h-10 w-10 items-center justify-center rounded-full border border-slate-700 bg-slate-900 active:bg-slate-800"
      >
        <UserRound color="#38bdf8" size={20} />
      </Pressable>

      <Modal
        visible={open}
        transparent
        animationType="fade"
        onRequestClose={() => setOpen(false)}
      >
        <TouchableWithoutFeedback onPress={() => setOpen(false)}>
          <View className="flex-1 bg-black/40">
            <TouchableWithoutFeedback>
              <View className="absolute right-5 top-14 w-52 rounded-2xl border border-slate-700 bg-slate-900 p-2 shadow-2xl">
                <View className="mb-2 border-b border-slate-800 px-3 py-2">
                  <Text className="text-xs font-bold uppercase tracking-wider text-slate-400">Library & Progress</Text>
                </View>
                {destinations.map(([name, Icon]) => (
                  <Pressable
                    key={name}
                    onPress={() => {
                      setOpen(false);
                      rootNavigation.navigate(name);
                    }}
                    className="flex-row items-center gap-3 rounded-xl px-3 py-3 active:bg-slate-800"
                  >
                    <View className="h-8 w-8 items-center justify-center rounded-lg bg-slate-800">
                      <Icon color="#38bdf8" size={18} />
                    </View>
                    <Text className="text-sm font-semibold text-slate-100">{name}</Text>
                  </Pressable>
                ))}
              </View>
            </TouchableWithoutFeedback>
          </View>
        </TouchableWithoutFeedback>
      </Modal>
    </View>
  );
}
