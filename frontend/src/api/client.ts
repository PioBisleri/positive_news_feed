import axios from 'axios';
import type { Article, ArticleFilters, Category } from '../types';

const client = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export async function fetchArticles(filters: ArticleFilters = {}): Promise<Article[]> {
    const params: Record<string, string | boolean> = {};
    if (filters.category) params.category = filters.category;
    if (filters.search) params.search = filters.search;
    if (filters.featured !== undefined) params.featured = filters.featured;

    const { data } = await client.get<Article[]>('/articles', { params });
    return data;
}

export async function fetchArticle(id: number): Promise<Article> {
    const { data } = await client.get<Article>(`/articles/${id}`);
    return data;
}

export async function toggleSave(id: number): Promise<Article> {
    const { data } = await client.patch<Article>(`/articles/${id}/save`);
    return data;
}

export async function addReaction(
    id: number,
    reactionType: string
): Promise<{ article_id: number; reaction_type: string; count: number }> {
    const { data } = await client.post<{
        article_id: number;
        reaction_type: string;
        count: number;
    }>(`/articles/${id}/react`, { reaction_type: reactionType });
    return data;
}

export async function fetchCategories(): Promise<Category[]> {
    const { data } = await client.get<Category[]>('/categories');
    return data;
}

export async function fetchSavedArticles(): Promise<Article[]> {
    const { data } = await client.get<Article[]>('/articles/saved');
    return data;
}

export default client;
