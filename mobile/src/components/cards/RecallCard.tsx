import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import type { FlashcardDTO, CardViewState } from '@/types/flashcard';
interface RecallCardProps {
    card: FlashcardDTO;
    viewState: CardViewState;
    onReveal: () => void;
}
export const RecallCard: React.FC<RecallCardProps> = ({
    card,
    viewState,
    onReveal,
}) => {
    const isRevealed = viewState.revealed;
    return (
        <ScrollView
            contentContainerStyle={styles.scrollContent}
            showsVerticalScrollIndicator={false}
        >
            {/* Question Section */}
            <View style={styles.questionSection}>
                <Text style={styles.promptLabel}>ACTIVE RECALL</Text>
                <Text style={styles.promptText}>
                    {card.prompt}
                </Text>
            </View>
            {/* Reveal Mechanism */}
            {!isRevealed ? (
                <TouchableOpacity
                    activeOpacity={0.8}
                    onPress={onReveal}
                    style={styles.revealTrigger}
                    accessibilityRole="button"
                    accessibilityLabel="Reveal answer"
                    accessibilityHint="Shows the answer after you have tried to recall it."
                >
                    <Text style={styles.revealIcon}>👁️</Text>
                    <Text style={styles.revealTitle}>Tap to Reveal Answer</Text>
                    <Text style={styles.revealSubtitle}>
                        Test yourself first before checking
                    </Text>
                </TouchableOpacity>
            ) : (
                <View style={styles.answerContainer}>
                    <View style={styles.answerHeader}>
                        <Text style={styles.answerBadge}>ANSWER</Text>
                    </View>
                    <Text style={styles.answerText}>{card.answer}</Text>
                    {card.explanation ? (
                        <View style={styles.explanationBox}>
                            <Text style={styles.explanationText}>
                                {card.explanation}
                            </Text>
                        </View>
                    ) : null}
                    {/* Key Points (if present) */}
                    {Array.isArray(card.key_points) && card.key_points.length > 0 && (
                        <View style={styles.keyPointsSection}>
                            <Text style={styles.keyPointsTitle}>KEY TAKEAWAYS</Text>
                            {card.key_points.map((pt, idx) => (
                                <View key={idx} style={styles.keyPointRow}>
                                    <Text style={styles.bulletDot}>•</Text>
                                    <Text style={styles.keyPointText}>{pt}</Text>
                                </View>
                            ))}
                        </View>
                    )}
                </View>
            )}
        </ScrollView>
    );
};
const styles = StyleSheet.create({
    scrollContent: {
        flexGrow: 1,
        justifyContent: 'center',
        paddingVertical: 8,
    },
    questionSection: {
        marginBottom: 20,
    },
    promptLabel: {
        color: '#38bdf8',
        fontSize: 11,
        fontWeight: '800',
        letterSpacing: 1,
        marginBottom: 8,
    },
    promptText: {
        color: '#f8fafc',
        fontSize: 21,
        fontWeight: '700',
        lineHeight: 29,
    },
    revealTrigger: {
        backgroundColor: '#131b2e',
        borderRadius: 18,
        borderWidth: 1.5,
        borderColor: '#1e293b',
        borderStyle: 'dashed',
        paddingVertical: 36,
        paddingHorizontal: 20,
        alignItems: 'center',
        justifyContent: 'center',
    },
    revealIcon: {
        fontSize: 32,
        marginBottom: 10,
    },
    revealTitle: {
        color: '#38bdf8',
        fontSize: 16,
        fontWeight: '700',
        marginBottom: 4,
    },
    revealSubtitle: {
        color: '#64748b',
        fontSize: 12,
    },
    answerContainer: {
        backgroundColor: '#131b2e',
        borderRadius: 18,
        borderWidth: 1,
        borderColor: '#38bdf8',
        padding: 20,
    },
    answerHeader: {
        marginBottom: 10,
    },
    answerBadge: {
        color: '#38bdf8',
        fontSize: 11,
        fontWeight: '800',
        letterSpacing: 0.5,
    },
    answerText: {
        color: '#f1f5f9',
        fontSize: 16,
        fontWeight: '600',
        lineHeight: 24,
    },
    explanationBox: {
        marginTop: 14,
        paddingTop: 12,
        borderTopWidth: 1,
        borderColor: '#1e293b',
    },
    explanationText: {
        color: '#94a3b8',
        fontSize: 14,
        lineHeight: 20,
        fontStyle: 'italic',
    },
    keyPointsSection: {
        marginTop: 16,
        paddingTop: 14,
        borderTopWidth: 1,
        borderColor: '#1e293b',
    },
    keyPointsTitle: {
        color: '#a78bfa',
        fontSize: 11,
        fontWeight: '800',
        letterSpacing: 0.5,
        marginBottom: 8,
    },
    keyPointRow: {
        flexDirection: 'row',
        alignItems: 'flex-start',
        marginBottom: 6,
    },
    bulletDot: {
        color: '#a78bfa',
        fontSize: 16,
        lineHeight: 20,
        marginRight: 8,
    },
    keyPointText: {
        color: '#cbd5e1',
        fontSize: 13,
        lineHeight: 19,
        flex: 1,
    },
});
