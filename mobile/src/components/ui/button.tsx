// mobile/src/components/ui/button.tsx
// NativeWind-styled button primitive inspired by shadcn/ui.
import React from 'react';
import { ActivityIndicator, Pressable, Text, type PressableProps } from 'react-native';

export type ButtonVariant = 'default' | 'secondary' | 'outline' | 'ghost' | 'destructive';
export type ButtonSize = 'sm' | 'default' | 'lg';

interface ButtonProps extends PressableProps {
    variant?: ButtonVariant;
    size?: ButtonSize;
    loading?: boolean;
    children: React.ReactNode;
    className?: string;
    textClassName?: string;
}

export const Button: React.FC<ButtonProps> = ({
    variant = 'default',
    size = 'default',
    loading = false,
    disabled = false,
    children,
    className = '',
    textClassName = '',
    ...props
}) => {
    const getVariantClasses = () => {
        switch (variant) {
            case 'secondary':
                return 'bg-slate-800 active:bg-slate-700 border border-slate-700';
            case 'outline':
                return 'bg-transparent border border-slate-700 active:bg-slate-800';
            case 'ghost':
                return 'bg-transparent active:bg-slate-800/60';
            case 'destructive':
                return 'bg-red-600 active:bg-red-500';
            case 'default':
            default:
                return 'bg-sky-500 active:bg-sky-400';
        }
    };

    const getTextVariantClasses = () => {
        switch (variant) {
            case 'secondary':
            case 'outline':
                return 'text-slate-100 font-semibold';
            case 'ghost':
                return 'text-slate-300 font-medium';
            case 'destructive':
                return 'text-white font-bold';
            case 'default':
            default:
                return 'text-slate-950 font-bold';
        }
    };

    const getSizeClasses = () => {
        switch (size) {
            case 'sm':
                return 'py-2 px-3 rounded-lg';
            case 'lg':
                return 'py-4 px-6 rounded-2xl';
            case 'default':
            default:
                return 'py-3 px-4 rounded-xl';
        }
    };

    const getTextSizeClasses = () => {
        switch (size) {
            case 'sm':
                return 'text-xs';
            case 'lg':
                return 'text-base';
            case 'default':
            default:
                return 'text-sm';
        }
    };

    const isInteractionDisabled = disabled || loading;

    return (
        <Pressable
            accessibilityRole="button"
            disabled={isInteractionDisabled}
            className={`flex-row items-center justify-center ${getSizeClasses()} ${getVariantClasses()} ${
                isInteractionDisabled ? 'opacity-50' : ''
            } ${className}`}
            {...props}
        >
            {loading ? (
                <ActivityIndicator
                    size="small"
                    color={variant === 'default' ? '#020617' : '#38bdf8'}
                    className="mr-2"
                />
            ) : null}
            {typeof children === 'string' ? (
                <Text className={`${getTextSizeClasses()} ${getTextVariantClasses()} ${textClassName}`}>
                    {children}
                </Text>
            ) : (
                children
            )}
        </Pressable>
    );
};
