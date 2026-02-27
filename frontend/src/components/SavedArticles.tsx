import React from 'react';
import type { Article } from '../types';
import NewsCard from './NewsCard';

interface SavedArticlesProps {
    articles: Article[];
    loading: boolean;
    error: string | null;
    onSaveToggle: (id: number, saved: boolean) => void;
}

const SavedArticles: React.FC<SavedArticlesProps> = ({ articles, loading, error, onSaveToggle }) => {
    if (loading) {
        return (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(3)].map((_, i) => (
                    <div key={i} className="bg-white rounded-2xl overflow-hidden shadow-card animate-pulse">
                        <div className="h-48 bg-amber-100" />
                        <div className="p-5 space-y-3">
                            <div className="h-3 bg-amber-100 rounded w-1/4" />
                            <div className="h-5 bg-gray-200 rounded w-3/4" />
                            <div className="h-3 bg-gray-100 rounded w-full" />
                            <div className="h-3 bg-gray-100 rounded w-5/6" />
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-center py-16">
                <span className="text-5xl mb-4 block">⚠️</span>
                <p className="text-red-500 font-medium">{error}</p>
            </div>
        );
    }

    if (articles.length === 0) {
        return (
            <div className="text-center py-24 animate-fade-in">
                <span className="text-8xl mb-6 block">🔖</span>
                <h2 className="text-2xl font-bold text-gray-700 mb-2">No saved stories yet</h2>
                <p className="text-gray-500 max-w-sm mx-auto">
                    When you find an uplifting story you love, tap the bookmark icon to save it here.
                </p>
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article) => (
                <NewsCard
                    key={article.id}
                    article={article}
                    onSaveToggle={onSaveToggle}
                />
            ))}
        </div>
    );
};

export default SavedArticles;
