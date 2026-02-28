import React from 'react';
import { AlertCircle, Bookmark } from 'lucide-react';
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
                    <div key={i} className="glass rounded-2xl overflow-hidden">
                        <div className="h-48 shimmer-bg" />
                        <div className="p-5 space-y-3">
                            <div className="h-3 shimmer-bg rounded-full w-1/4" />
                            <div className="h-5 shimmer-bg rounded-lg w-3/4" />
                            <div className="h-3 shimmer-bg rounded-full" />
                            <div className="h-3 shimmer-bg rounded-full w-5/6" />
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    if (error) {
        return (
            <div className="glass border border-red-500/20 text-red-300 rounded-2xl p-6 flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" strokeWidth={1.5} />
                <p className="font-medium">{error}</p>
            </div>
        );
    }

    if (articles.length === 0) {
        return (
            <div className="text-center py-24 animate-fade-in">
                <div className="inline-block glass rounded-3xl p-12 max-w-sm">
                    <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-sky-500/20 to-emerald-500/20 border border-white/10 flex items-center justify-center mx-auto mb-5">
                        <Bookmark className="w-7 h-7 text-sky-400" strokeWidth={1.5} />
                    </div>
                    <h2 className="text-2xl font-bold text-white mb-3">No saved stories yet</h2>
                    <p className="text-slate-400 text-sm leading-relaxed">
                        When you find an uplifting story you love, tap the{' '}
                        <span className="text-sky-400 font-semibold">bookmark</span> icon to save it here.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article) => (
                <NewsCard key={article.id} article={article} onSaveToggle={onSaveToggle} />
            ))}
        </div>
    );
};

export default SavedArticles;
