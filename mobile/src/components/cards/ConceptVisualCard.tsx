import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import type { FlashcardDTO } from '@/types/flashcard';
interface ConceptVisualCardProps {
    card: FlashcardDTO;
}
export const ConceptVisualCard: React.FC<ConceptVisualCardProps> = ({ card }) => {
    return (
        <ScrollView
            contentContainerStyle={styles.scrollContent}
            showsVerticalScrollIndicator={false}
        >
            {/* Visual Header / Diagram Anchor */}
            <View style={styles.visualContainer}>
                <View style={styles.visualIconBox}>
                    <Text style={styles.visualIconText}>
                        {card.visual_hint || '💡'}
                    </Text>
                </View>
                {card.concept_name && (
                    <Text style={styles.visualCaption}>
                        Core Concept: {card.concept_name}
                    </Text>
                )}
            </View>
            {/* Prompt / Statement */}
            <Text style={styles.titleText}>
                {card.title || card.prompt}
            </Text>
            {/* Explanation / Breakdown */}
            <View style={styles.cardBox}>
                <Text style={styles.bodyText}>
                    {card.explanation || card.answer}
                </Text>
            </View>
            {/* Canonical Claim Quote (if available) */}
            {card.canonical_claim_text && (
                <View style={styles.provenanceBox}>
                    <Text style={styles.provenanceLabel}>VERIFIED CLAIM</Text>
                    <Text style={styles.provenanceText}>
                        "{card.canonical_claim_text}"
                    </Text>
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
    visualContainer: {
        alignItems: 'center',
        marginBottom: 20,
    },
    visualIconBox: {
        width: 88,
        height: 88,
        borderRadius: 24,
        backgroundColor: '#1e293b',
        borderWidth: 1.5,
        borderColor: '#6366f1',
        justifyContent: 'center',
        alignItems: 'center',
        shadowColor: '#6366f1',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 10,
        elevation: 6,
    },
    visualIconText: {
        fontSize: 36,
    },
    visualCaption: {
        color: '#94a3b8',
        fontSize: 12,
        fontWeight: '600',
        marginTop: 8,
        textTransform: 'uppercase',
        letterSpacing: 0.8,
    },
    titleText: {
        color: '#f8fafc',
        fontSize: 22,
        fontWeight: '800',
        lineHeight: 28,
        textAlign: 'center',
        marginBottom: 16,
    },
    cardBox: {
        backgroundColor: '#131b2e',
        borderRadius: 16,
        padding: 18,
        borderWidth: 1,
        borderColor: '#1e293b',
        marginBottom: 16,
    },
    bodyText: {
        color: '#cbd5e1',
        fontSize: 15,
        lineHeight: 23,
    },
    provenanceBox: {
        backgroundColor: 'rgba(56, 189, 248, 0.08)',
        borderLeftWidth: 3,
        borderLeftColor: '#38bdf8',
        paddingHorizontal: 14,
        paddingVertical: 10,
        borderRadius: 8,
    },
    provenanceLabel: {
        color: '#38bdf8',
        fontSize: 10,
        fontWeight: '800',
        letterSpacing: 0.5,
        marginBottom: 4,
    },
    provenanceText: {
        color: '#94a3b8',
        fontSize: 12,
        fontStyle: 'italic',
        lineHeight: 18,
    },
});