// Public flashcard feed
// Displays cards with concept tag, canonical claim, and provenance indicator.
// Backend Endpoint: GET /api/learning/feed/

import React, { useCallback, useMemo, useRef, useState } from 'react';
import { useFocusEffect } from '@react-navigation/native';
import { ProfileMenu } from '@/components/ProfileMenu';
import {
    ActivityIndicator,
    FlatList,
    RefreshControl,
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
    ViewToken,
} from 'react-native';
import { CardRenderer } from '@/components/cards';
import { useFlashcardFeed } from '@/hooks/useFlashcardFeed';
import type { FlashcardDTO } from '@/types/flashcard';

export default function FeedScreen({ navigation }: any) {
    const feed = useFlashcardFeed();
    const [viewportHeight, setViewportHeight] = useState(0);
    const listRef = useRef<FlatList<FlashcardDTO>>(null);
    const onCardVisibleRef = useRef(feed.onCardVisible);
    onCardVisibleRef.current = feed.onCardVisible;

    const viewabilityConfig = useRef({
        itemVisiblePercentThreshold: 80,
        minimumViewTime: 100,
    }).current;

    const onViewableItemsChanged = useRef(
        ({ viewableItems }: { viewableItems: ViewToken[] }) => {
            const index = viewableItems.find(token => token.isViewable)?.index;
            if (typeof index === 'number') {
                onCardVisibleRef.current(index);
            }
        },
    ).current;

    const renderItem = useCallback(({ item }: { item: FlashcardDTO }) => (
        <View style={{ height: viewportHeight }}>
            <CardRenderer
                card={item}
                viewState={feed.viewStates[item.id]}
                cardHeight={viewportHeight}
                onRevealAnswer={feed.revealAnswer}
                onSelectOption={feed.selectOption}
                onToggleSave={id => navigation.navigate('PlaylistModal', { flashcardId: id })}
                onMarkUnderstood={feed.markUnderstood}
                onOpenDetail={id => navigation.navigate('FlashcardDetail', { id })}
                onOpenExplain={claimId =>
                    navigation.navigate('GroundedExplain', { claimId })
                }
            />
        </View>
    ), [
        feed.viewStates,
        feed.revealAnswer,
        feed.selectOption,
        feed.markUnderstood,
        navigation,
        viewportHeight,
    ]);

    const getItemLayout = useCallback(
        (_: ArrayLike<FlashcardDTO> | null | undefined, index: number) => ({
            length: viewportHeight,
            offset: viewportHeight * index,
            index,
        }),
        [viewportHeight],
    );

    const progressWidth = useMemo(() => {
        if (!feed.cards.length) return '0%' as `${number}%`;
        return `${((feed.currentIndex + 1) / feed.cards.length) * 100}%` as `${number}%`;
    }, [feed.currentIndex, feed.cards.length]);

    const refreshFeed = useCallback(() => {
        listRef.current?.scrollToOffset({ offset: 0, animated: false });
        feed.refresh();
    }, [feed.refresh]);

    const hasOpenedRef = useRef(false);
    useFocusEffect(useCallback(() => {
        if (hasOpenedRef.current) refreshFeed();
        hasOpenedRef.current = true;
    }, [refreshFeed]));

    if (feed.status === 'idle' || feed.status === 'loading') {
        return (
            <View style={styles.center}>
                <ActivityIndicator size="large" color="#38bdf8" />
                <Text style={styles.secondary}>Curating your flashcard feed...</Text>
            </View>
        );
    }

    if (feed.status === 'error' && feed.cards.length === 0) {
        return (
            <View style={styles.center}>
                <Text style={styles.title}>Couldn’t load the feed</Text>
                <Text style={styles.secondary}>{feed.error}</Text>
                <TouchableOpacity style={styles.retry} onPress={refreshFeed}>
                    <Text style={styles.retryText}>Try again</Text>
                </TouchableOpacity>
            </View>
        );
    }

    return (
        <View
            style={styles.container}
            onLayout={event => {
                const height = event.nativeEvent.layout.height;
                setViewportHeight(current => current === height ? current : height);
            }}
        >
            {viewportHeight > 0 && feed.cards.length > 0 && (
                <>
                    <FlatList
                        ref={listRef}
                        data={feed.cards}
                        keyExtractor={item => String(item.id)}
                        renderItem={renderItem}
                        extraData={feed.viewStates}
                        pagingEnabled
                        snapToInterval={viewportHeight}
                        decelerationRate="fast"
                        showsVerticalScrollIndicator={false}
                        initialNumToRender={2}
                        maxToRenderPerBatch={2}
                        windowSize={3}
                        getItemLayout={getItemLayout}
                        onViewableItemsChanged={onViewableItemsChanged}
                        viewabilityConfig={viewabilityConfig}
                        onEndReachedThreshold={0.5}
                        onEndReached={() => {
                            if (!feed.sessionExhausted && !feed.isLoadingMore) {
                                feed.loadMore();
                            }
                        }}
                        accessibilityRole="list"
                        refreshControl={
                            <RefreshControl
                                refreshing={feed.status === 'refreshing'}
                                onRefresh={refreshFeed}
                                tintColor="#38bdf8"
                            />
                        }
                    />

                    <View style={styles.profileControl}><ProfileMenu navigation={navigation} /></View>

                    {feed.sessionComplete && (
                        <View pointerEvents="none" style={styles.endHint}>
                            <Text style={styles.endHintText}>You’ve viewed every card · pull down to refresh</Text>
                        </View>
                    )}
                </>
            )}

            {feed.cards.length === 0 && feed.status !== 'refreshing' && (
                <View style={styles.center}>
                    <Text style={styles.title}>No flashcards yet</Text>
                    <Text style={styles.secondary}>
                        Cards appear after knowledge is verified and supported. Upload a note to start the review process.
                    </Text>
                    <TouchableOpacity style={styles.retry} onPress={() => navigation.navigate('Upload')}>
                        <Text style={styles.retryText}>Upload a note</Text>
                    </TouchableOpacity>
                    <TouchableOpacity onPress={refreshFeed} accessibilityRole="button" accessibilityLabel="Refresh feed">
                        <Text style={styles.secondary}>Refresh feed</Text>
                    </TouchableOpacity>
                </View>
            )}

            {feed.status === 'error' && feed.cards.length > 0 && (
                <View style={styles.inlineError}>
                    <Text style={styles.inlineErrorText}>
                        Refresh failed: {feed.error}
                    </Text>
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#090d16' },
    center: {
        flex: 1,
        backgroundColor: '#090d16',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 28,
    },
    title: { color: '#f8fafc', fontSize: 20, fontWeight: '800', textAlign: 'center' },
    secondary: { color: '#94a3b8', marginTop: 12, textAlign: 'center', lineHeight: 21 },
    retry: {
        marginTop: 20,
        backgroundColor: '#1e293b',
        paddingHorizontal: 18,
        paddingVertical: 10,
        borderRadius: 10,
    },
    retryText: { color: '#e2e8f0', fontWeight: '700' },
    progressTrack: {
        position: 'absolute',
        top: 0,
        left: 20,
        right: 20,
        height: 3,
        backgroundColor: '#1e293b',
        borderRadius: 2,
    },
    progressFill: { height: 3, backgroundColor: '#38bdf8', borderRadius: 2 },
    profileControl: {
        position: 'absolute',
        top: 12,
        right: 20,
        backgroundColor: 'rgba(9, 13, 22, 0.72)',
        paddingHorizontal: 10,
        paddingVertical: 5,
        borderRadius: 12,
    },
    endHint: {
        position: 'absolute',
        bottom: 12,
        alignSelf: 'center',
        backgroundColor: 'rgba(9, 13, 22, 0.78)',
        paddingHorizontal: 12,
        paddingVertical: 7,
        borderRadius: 14,
    },
    endHintText: { color: '#cbd5e1', fontSize: 11 },
    inlineError: {
        position: 'absolute',
        top: 22,
        left: 20,
        right: 20,
        padding: 10,
        backgroundColor: '#7f1d1d',
        borderRadius: 8,
    },
    inlineErrorText: { color: '#fee2e2', fontSize: 12, textAlign: 'center' },
});
