export interface Category {
    id: number;
    name: string;
    emoji: string | null;
    color: string | null;
}

export interface Reaction {
    id: number;
    article_id: number;
    reaction_type: string;
    count: number;
}

export interface Article {
    id: number;
    title: string;
    summary: string;
    content: string | null;
    image_url: string | null;
    source: string | null;
    author: string | null;
    published_at: string | null;
    category_id: number | null;
    is_featured: boolean;
    is_saved: boolean;
    created_at: string | null;
    category: Category | null;
    reactions: Reaction[];
}

export interface ArticleFilters {
    category?: string;
    search?: string;
    featured?: boolean;
}

export type ReactionType = 'inspiring' | 'heartwarming' | 'amazing' | 'hopeful';

export const REACTION_META: Record<ReactionType, { emoji: string; label: string }> = {
    inspiring: { emoji: '🌟', label: 'Inspiring' },
    heartwarming: { emoji: '🤗', label: 'Heartwarming' },
    amazing: { emoji: '🎉', label: 'Amazing' },
    hopeful: { emoji: '🌱', label: 'Hopeful' },
};
