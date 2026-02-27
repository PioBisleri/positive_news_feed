export interface Category {
    id: number;
    name: string;
    emoji: string | null;
    color: string | null;
}

export interface Article {
    id: number;
    title: string;
    summary: string;
    content: string | null;
    image_url: string | null;
    url: string | null;
    source: string | null;
    author: string | null;
    published_at: string | null;
    category_id: number | null;
    is_featured: boolean;
    is_saved: boolean;
    created_at: string | null;
    category: Category | null;
}

export interface ArticleFilters {
    category?: string;
    search?: string;
    featured?: boolean;
}
