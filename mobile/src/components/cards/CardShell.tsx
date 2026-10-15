import React from 'react';
import {
    View,
    Text,
    TouchableOpacity,
    StyleSheet,
    Dimensions,
} from 'react-native';
import type { FlashcardDTO } from '@/types/flashcard';

const { height: WINDOW_HEIGHT } = Dimensions.get('window');

interface CardShellProps {
    card: FlashcardDTO;
    children: React.ReactNode;
    isUnderstood?: boolean;
    isSaved?: boolean;
    onToggleUnderstood?: () => void;
    onToggleSave?: () => void;
    onOpenExplain?: () => void;
    onOpenDetail?: () => void;
    cardHeight?: number;
}

export const CardShell: React.FC<CardShellProps> = ({
    card,
    children,
    isUnderstood = false,
    isSaved = false,
    onToggleUnderstood,
    onToggleSave,
    onOpenExplain,
    onOpenDetail,
    cardHeight = WINDOW_HEIGHT,
}) => {
    return (
        <View style={[styles.container, { height: cardHeight }]}>
            {/* Top Meta Bar */}
            <View style={styles.topBar}>
                <View style={styles.badgeRow}>
                    {card.concept_name && (
                        <View style={styles.conceptBadge}>
                            <Text style={styles.conceptBadgeText} numberOfLines={1}>
                                {card.concept_name}
                            </Text>
                        </View>
                    )}
                    <View style={[styles.typeBadge, getTypeBadgeStyle(card.card_type)]}>
                        <Text style={styles.typeBadgeText}>
                            {formatCardType(card.card_type)}
                        </Text>
                    </View>
                    <View style={[styles.diffBadge, getDifficultyStyle(card.difficulty)]}>
                        <Text style={styles.diffText}>
                            {card.difficulty?.toUpperCase() || 'CORE'}
                        </Text>
                    </View>
                </View>
            </View>
            {/* Template Content Slot */}
            <View style={styles.contentSlot}>
                {children}
            </View>
            {/* Bottom Action Bar */}
            <View style={styles.bottomBar}>
                <View style={styles.actionLeft}>
                    {onToggleUnderstood && (
                        <TouchableOpacity
                            activeOpacity={0.75}
                            onPress={onToggleUnderstood}
                            style={[
                                styles.actionBtn,
                                isUnderstood && styles.actionBtnUnderstood,
                            ]}
                        >
                            <Text
                                style={[
                                    styles.actionBtnText,
                                    isUnderstood && styles.actionBtnTextActive,
                                ]}
                            >
                                {isUnderstood ? '✓ Understood' : 'Mark Understood'}
                            </Text>
                        </TouchableOpacity>
                    )}
                    {onToggleSave && (
                        <TouchableOpacity
                            activeOpacity={0.75}
                            onPress={onToggleSave}
                            style={[
                                styles.actionBtn,
                                isSaved && styles.actionBtnSaved,
                            ]}
                        >
                            <Text
                                style={[
                                    styles.actionBtnText,
                                    isSaved && styles.actionBtnTextSaved,
                                ]}
                            >
                                {isSaved ? '★ Saved' : '☆ Save'}
                            </Text>
                        </TouchableOpacity>
                    )}
                </View>
                <View style={styles.actionRight}>
                    {card.canonical_claim_id && onOpenExplain && (
                        <TouchableOpacity
                            activeOpacity={0.75}
                            onPress={onOpenExplain}
                            style={styles.iconBtn}
                            accessibilityLabel="View Grounded Explanation"
                        >
                            <Text style={styles.iconBtnText}>📖 Explain</Text>
                        </TouchableOpacity>
                    )}
                    {onOpenDetail && (
                        <TouchableOpacity
                            activeOpacity={0.75}
                            onPress={onOpenDetail}
                            style={styles.iconBtn}
                            accessibilityLabel="Card Details"
                        >
                            <Text style={styles.iconBtnText}>ℹ️</Text>
                        </TouchableOpacity>
                    )}
                </View>
            </View>
        </View>
    );
};
function formatCardType(type: string): string {
    if (type === 'concept_visual') return 'VISUAL';
    if (type === 'quick_quiz') return 'QUIZ';
    return 'RECALL';
}
function getTypeBadgeStyle(type: string) {
    if (type === 'concept_visual') return { backgroundColor: '#6366f1' };
    if (type === 'quick_quiz') return { backgroundColor: '#d97706' };
    return { backgroundColor: '#0284c7' };
}
function getDifficultyStyle(diff: string) {
    if (diff === 'advanced') return { backgroundColor: '#7f1d1d' };
    if (diff === 'intermediate') return { backgroundColor: '#78350f' };
    return { backgroundColor: '#064e3b' };
}
const styles = StyleSheet.create({
    container: {
        width: '100%',
        backgroundColor: '#090d16',
        paddingHorizontal: 20,
        paddingTop: 12,
        paddingBottom: 24,
        justifyContent: 'space-between',
    },
    topBar: {
        paddingTop: 8,
        paddingBottom: 12,
    },
    badgeRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
        flexWrap: 'wrap',
    },
    conceptBadge: {
        backgroundColor: '#1e293b',
        borderWidth: 1,
        borderColor: '#38bdf8',
        paddingHorizontal: 12,
        paddingVertical: 5,
        borderRadius: 20,
        maxWidth: '50%',
    },
    conceptBadgeText: {
        color: '#38bdf8',
        fontSize: 12,
        fontWeight: '700',
    },
    typeBadge: {
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 6,
    },
    typeBadgeText: {
        color: '#ffffff',
        fontSize: 10,
        fontWeight: '800',
        letterSpacing: 0.5,
    },
    diffBadge: {
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 6,
    },
    diffText: {
        color: '#f8fafc',
        fontSize: 10,
        fontWeight: '700',
    },
    contentSlot: {
        flex: 1,
        justifyContent: 'center',
        marginVertical: 12,
    },
    bottomBar: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingTop: 14,
        borderTopWidth: 1,
        borderColor: '#1e293b',
    },
    actionLeft: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
    },
    actionRight: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
    },
    actionBtn: {
        backgroundColor: '#1e293b',
        paddingHorizontal: 14,
        paddingVertical: 8,
        borderRadius: 10,
        borderWidth: 1,
        borderColor: '#334155',
    },
    actionBtnUnderstood: {
        backgroundColor: '#059669',
        borderColor: '#10b981',
    },
    actionBtnSaved: {
        backgroundColor: '#78350f',
        borderColor: '#f59e0b',
    },
    actionBtnText: {
        color: '#94a3b8',
        fontSize: 13,
        fontWeight: '600',
    },
    actionBtnTextActive: {
        color: '#ffffff',
        fontWeight: '700',
    },
    actionBtnTextSaved: {
        color: '#fde68a',
        fontWeight: '700',
    },
    iconBtn: {
        backgroundColor: '#1e293b',
        paddingHorizontal: 10,
        paddingVertical: 8,
        borderRadius: 8,
    },
    iconBtnText: {
        color: '#cbd5e1',
        fontSize: 12,
        fontWeight: '600',
    },
});