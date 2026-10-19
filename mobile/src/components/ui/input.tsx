// mobile/src/components/ui/input.tsx
// Dark-mode themed TextInput primitive.
import React from 'react';
import { TextInput, View, Text, type TextInputProps } from 'react-native';

interface InputProps extends TextInputProps {
    label?: string;
    error?: string;
    containerClassName?: string;
}

export const Input: React.FC<InputProps> = ({
    label,
    error,
    containerClassName = '',
    className = '',
    placeholderTextColor = '#64748b',
    ...props
}) => {
    return (
        <View className={`w-full ${containerClassName}`}>
            {label ? (
                <Text className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    {label}
                </Text>
            ) : null}
            <TextInput
                placeholderTextColor={placeholderTextColor}
                className={`w-full bg-slate-900 border ${
                    error ? 'border-red-500' : 'border-slate-700 focus:border-sky-500'
                } rounded-xl px-4 py-3 text-base text-slate-100 ${className}`}
                {...props}
            />
            {error ? (
                <Text className="text-xs text-red-400 mt-1 font-medium">{error}</Text>
            ) : null}
        </View>
    );
};
