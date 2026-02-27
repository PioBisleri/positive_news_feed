import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import type { Article } from '../types';
import { fetchArticle, toggleSave } from '../api/client';
import ReactionBar from '../components/ReactionBar';

const formatDate = (dateStr: string | null): string => {
    if (!dateStr) return '';
    return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });
};

const getCategoryStyles = (color: string | null): string =>
    color ?? 'bg-amber-100 text-amber-800';

const ArticlePage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [article, setArticle] = useState<Article | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        if (!id) return;
        setLoading(true);
        fetchArticle(Number(id))
            .then(setArticle)
            .catch(() => setError('Could not load this article.'))
            .finally(() => setLoading(false));
    }, [id]);

    const handleSave = async () => {
        if (!article || saving) return;
        setSaving(true);
        try {
            const updated = await toggleSave(article.id);
            setArticle((prev) => (prev ? { ...prev, is_saved: updated.is_saved } : prev));
        } catch {
            // ignore
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="max-w-4xl mx-auto px-4 py-10 animate-pulse">
                <div className="h-80 bg-amber-100 rounded-2xl mb-8" />
                <div className="h-4 bg-amber-100 rounded w-1/5 mb-4" />
                <div className="h-8 bg-gray-200 rounded w-3/4 mb-6" />
                <div className="space-y-3">
                    {[...Array(6)].map((_, i) => (
                        <div key={i} className="h-4 bg-gray-100 rounded w-full" />
                    ))}
                </div>
            </div>
        );
    }

    if (error || !article) {
        return (
            <div className="text-center py-24">
                <span className="text-6xl block mb-4">😔</span>
                <p className="text-red-500 font-medium text-lg">{error ?? 'Article not found.'}</p>
                <button
                    onClick={() => navigate('/')}
                    className="mt-6 px-6 py-2 bg-amber-500 text-white font-semibold rounded-full hover:bg-amber-600 transition-colors"
                >
                    ← Back to Home
                </button>
            </div>
        );
    }

    const paragraphs = article.content
        ? article.content.split(/\n\n+/).filter(Boolean)
        : [article.summary];

    return (
        <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 animate-fade-in">
            {/* Back button */}
            <button
                onClick={() => navigate(-1)}
                className="flex items-center gap-2 text-amber-700 font-semibold mb-6 hover:text-amber-900 transition-colors group"
            >
                <span className="transition-transform group-hover:-translate-x-1">←</span>
                Back
            </button>

            {/* Hero Image */}
            {article.image_url ? (
                <div className="rounded-2xl overflow-hidden mb-8 h-64 sm:h-96">
                    <img
                        src={article.image_url}
                        alt={article.title}
                        className="w-full h-full object-cover"
                    />
                </div>
            ) : (
                <div className="rounded-2xl bg-gradient-to-br from-amber-200 to-orange-100 flex items-center justify-center mb-8 h-64">
                    <span className="text-8xl opacity-60">{article.category?.emoji ?? '📰'}</span>
                </div>
            )}

            {/* Meta */}
            <div className="flex flex-wrap items-center gap-3 mb-4">
                {article.category && (
                    <span
                        className={`text-sm font-semibold px-3 py-1 rounded-full ${getCategoryStyles(article.category.color)}`}
                    >
                        {article.category.emoji} {article.category.name}
                    </span>
                )}
                {article.is_featured && (
                    <span className="bg-amber-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                        ⭐ Featured
                    </span>
                )}
            </div>

            {/* Title */}
            <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900 leading-tight mb-4">
                {article.title}
            </h1>

            {/* Author / Source / Date */}
            <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 mb-8 pb-6 border-b border-gray-100">
                {article.author && (
                    <span className="font-medium text-gray-700">✍️ {article.author}</span>
                )}
                {article.source && <span>📰 {article.source}</span>}
                {article.published_at && <span>🗓️ {formatDate(article.published_at)}</span>}
            </div>

            {/* Content */}
            <div className="prose prose-lg max-w-none mb-10">
                {paragraphs.map((para, idx) => (
                    <p key={idx} className="text-gray-700 leading-relaxed text-lg mb-5">
                        {para.trim()}
                    </p>
                ))}
            </div>

            {/* Reaction Bar */}
            <div className="bg-amber-50 rounded-2xl p-6 mb-6">
                <h3 className="text-sm font-bold text-gray-600 uppercase tracking-wide mb-4">
                    How did this story make you feel?
                </h3>
                <ReactionBar articleId={article.id} reactions={article.reactions} size="lg" />
            </div>

            {/* Save Button */}
            <div className="flex justify-end">
                <button
                    onClick={handleSave}
                    disabled={saving}
                    className={`flex items-center gap-2 px-6 py-3 rounded-full font-semibold text-sm transition-all duration-200
            hover:scale-105 active:scale-95
            ${article.is_saved
                            ? 'bg-amber-500 text-white shadow-md hover:bg-amber-600'
                            : 'bg-white border border-gray-200 text-gray-600 hover:border-amber-400 hover:text-amber-700'
                        }
            ${saving ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                    🔖 {article.is_saved ? 'Saved!' : 'Save Story'}
                </button>
            </div>
        </div>
    );
};

export default ArticlePage;
