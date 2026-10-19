// mobile/src/components/ui/badge.tsx
// Badge / Pill component for concepts, status, and difficulties.
import React from 'react';
import { View, Text } from 'react-native';

export type BadgeVariant = 'default' | 'accent' | 'success' | 'warning' | 'destructive' | 'outline';

interface BadgeProps {
    variant?: BadgeVariant;
    children: React.ReactNode;
    className?: string;
    textClassName?: string;
}

export const Badge: React.FC<BadgeProps> = ({
    variant = 'default',
    children,
    className = '',
    textClassName = '',
}) => {
    const getBadgeStyle = () => {
        switch (variant) {
            case 'accent':
                return { bg: 'bg-sky-950/80 border-sky-600/80', text: 'text-sky-300' };
            case 'success':
                return { bg: 'bg-emerald-950/80 border-emerald-600/80', text: 'text-emerald-300' };
            case 'warning':
                return { bg: 'bg-amber-950/80 border-amber-600/80', text: 'text-amber-300' };
            case 'destructive':
                return { bg: 'bg-red-950/80 border-red-600/80', text: 'text-red-300' };
            case 'outline':
                return { bg: 'bg-transparent border-slate-700', text: 'text-slate-300' };
            case 'default':
            default:
                return { bg: 'bg-slate-800 border-slate-700', text: 'text-slate-200' };
        }
    };

    const style = getBadgeStyle();

    return (
        <View className={`self-start px-2.5 py-1 rounded-full border ${style.bg} ${className}`}>
            {typeof children === 'string' ? (
                <Text className={`text-xs font-bold tracking-wide ${style.text} ${textClassName}`}>
                    {children}
                </Text>
            ) : (
                children
            )}
        </View>
    );
};
