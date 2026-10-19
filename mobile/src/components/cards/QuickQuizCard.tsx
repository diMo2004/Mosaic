import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import type { FlashcardDTO, CardViewState } from '@/types/flashcard';
interface QuickQuizCardProps {
    card: FlashcardDTO;
    viewState: CardViewState;
    onSelectOption: (index: number) => void;
}
export const QuickQuizCard: React.FC<QuickQuizCardProps> = ({
    card,
    viewState,
    onSelectOption,
}) => {
    const isAnswered = viewState.answered;
    const selectedIdx = viewState.selectedOption;
    const options = card.quiz_options || [];
    return (
        <ScrollView
            contentContainerStyle={styles.scrollContent}
            showsVerticalScrollIndicator={false}
        >
            <View style={styles.headerBox}>
                <Text style={styles.quizLabel}>QUICK QUIZ</Text>
                <Text style={styles.questionText}>
                    {card.prompt}
                </Text>
            </View>
            {/* Options List */}
            <View style={styles.optionsList}>
                {options.map((option, idx) => {
                    const isSelected = selectedIdx === idx;
                    const isCorrect = option.is_correct;
                    let btnStyle = styles.optionBtn;
                    let textStyle = styles.optionText;
                    let badgeText = String.fromCharCode(65 + idx); // A, B, C, D
                    if (isAnswered) {
                        if (isCorrect) {
                            btnStyle = styles.optionBtnCorrect;
                            textStyle = styles.optionTextCorrect;
                            badgeText = '✓';
                        } else if (isSelected && !isCorrect) {
                            btnStyle = styles.optionBtnIncorrect;
                            textStyle = styles.optionTextIncorrect;
                            badgeText = '✗';
                        } else {
                            btnStyle = styles.optionBtnDimmed;
                            textStyle = styles.optionTextDimmed;
                        }
                    } else if (isSelected) {
                        btnStyle = styles.optionBtnSelected;
                    }
                    return (
                        <TouchableOpacity
                            key={idx}
                            activeOpacity={isAnswered ? 1 : 0.75}
                            disabled={isAnswered}
                            onPress={() => onSelectOption(idx)}
                            style={[styles.baseOption, btnStyle]}
                            accessibilityRole="button"
                            accessibilityLabel={`Option ${String.fromCharCode(65 + idx)}: ${option.text}`}
                            accessibilityState={{
                                selected: isSelected,
                                disabled: isAnswered,
                            }}
                            accessibilityHint={isAnswered ? undefined : 'Select this answer.'}
                        >
                            <View style={styles.badgeCircle}>
                                <Text style={styles.badgeCircleText}>{badgeText}</Text>
                            </View>
                            <Text style={[styles.baseText, textStyle]}>
                                {option.text}
                            </Text>
                        </TouchableOpacity>
                    );
                })}
            </View>
            {/* Explanation Post-Answer */}
            {isAnswered && (
                <View style={styles.feedbackContainer}>
                    <Text style={styles.feedbackTitle}>
                        {selectedIdx !== null && options[selectedIdx]?.is_correct
                            ? '🎉 Correct!'
                            : '💡 Concept Review'}
                    </Text>
                    {selectedIdx !== null && options[selectedIdx]?.explanation ? (
                        <Text style={styles.feedbackText}>
                            {options[selectedIdx].explanation}
                        </Text>
                    ) : (
                        <Text style={styles.feedbackText}>
                            {card.explanation || card.answer}
                        </Text>
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
    headerBox: {
        marginBottom: 16,
    },
    quizLabel: {
        color: '#f59e0b',
        fontSize: 11,
        fontWeight: '800',
        letterSpacing: 1,
        marginBottom: 6,
    },
    questionText: {
        color: '#f8fafc',
        fontSize: 19,
        fontWeight: '700',
        lineHeight: 26,
    },
    optionsList: {
        gap: 10,
        marginVertical: 12,
    },
    baseOption: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 14,
        borderRadius: 14,
        borderWidth: 1.5,
    },
    optionBtn: {
        backgroundColor: '#131b2e',
        borderColor: '#1e293b',
    },
    optionBtnSelected: {
        backgroundColor: '#1e293b',
        borderColor: '#38bdf8',
    },
    optionBtnCorrect: {
        backgroundColor: 'rgba(5, 150, 105, 0.18)',
        borderColor: '#10b981',
    },
    optionBtnIncorrect: {
        backgroundColor: 'rgba(239, 68, 68, 0.18)',
        borderColor: '#ef4444',
    },
    optionBtnDimmed: {
        backgroundColor: '#0c121f',
        borderColor: '#172033',
        opacity: 0.5,
    },
    badgeCircle: {
        width: 28,
        height: 28,
        borderRadius: 14,
        backgroundColor: '#1e293b',
        alignItems: 'center',
        justifyContent: 'center',
        marginRight: 12,
    },
    badgeCircleText: {
        color: '#cbd5e1',
        fontSize: 12,
        fontWeight: '700',
    },
    baseText: {
        fontSize: 14,
        lineHeight: 20,
        flex: 1,
    },
    optionText: {
        color: '#e2e8f0',
    },
    optionTextCorrect: {
        color: '#34d399',
        fontWeight: '700',
    },
    optionTextIncorrect: {
        color: '#f87171',
        fontWeight: '600',
    },
    optionTextDimmed: {
        color: '#64748b',
    },
    feedbackContainer: {
        marginTop: 14,
        padding: 14,
        backgroundColor: '#131b2e',
        borderRadius: 12,
        borderLeftWidth: 3,
        borderLeftColor: '#38bdf8',
    },
    feedbackTitle: {
        color: '#f8fafc',
        fontSize: 14,
        fontWeight: '700',
        marginBottom: 4,
    },
    feedbackText: {
        color: '#94a3b8',
        fontSize: 13,
        lineHeight: 19,
    },
});
