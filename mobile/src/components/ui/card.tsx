// mobile/src/components/ui/card.tsx
// Composable Card surface primitive following shadcn/ui patterns.
import React from 'react';
import { View, Text, type ViewProps } from 'react-native';

interface CardProps extends ViewProps {
    className?: string;
    children: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ className = '', children, ...props }) => (
    <View
        className={`bg-panel border border-slate-800 rounded-2xl p-5 shadow-sm ${className}`}
        {...props}
    >
        {children}
    </View>
);

export const CardHeader: React.FC<CardProps> = ({ className = '', children, ...props }) => (
    <View className={`mb-3 ${className}`} {...props}>
        {children}
    </View>
);

export const CardTitle: React.FC<{ className?: string; children: React.ReactNode }> = ({
    className = '',
    children,
}) => (
    <Text className={`text-lg font-bold text-slate-50 ${className}`}>{children}</Text>
);

export const CardDescription: React.FC<{ className?: string; children: React.ReactNode }> = ({
    className = '',
    children,
}) => (
    <Text className={`text-sm text-slate-400 mt-1 leading-relaxed ${className}`}>{children}</Text>
);

export const CardContent: React.FC<CardProps> = ({ className = '', children, ...props }) => (
    <View className={`my-2 ${className}`} {...props}>
        {children}
    </View>
);

export const CardFooter: React.FC<CardProps> = ({ className = '', children, ...props }) => (
    <View className={`mt-3 pt-3 border-t border-slate-800 flex-row items-center justify-between ${className}`} {...props}>
        {children}
    </View>
);
