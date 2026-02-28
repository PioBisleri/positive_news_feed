import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Bookmark, Star, Pen, Newspaper, Calendar } from 'lucide-react';
import type { Article } from '../types';
import { fetchArticle, toggleSave } from '../api/client';

const formatDate = (dateStr: string | null): string => {
    if (!dateStr) return '';
    return new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
};

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
        } catch { /* ignore */ }
        finally { setSaving(false); }
    };

    if (loading) {
        return (
            <div className="max-w-4xl mx-auto px-4 py-10">
                <div className="h-80 shimmer-bg rounded-2xl mb-8" />
                <div className="h-4 shimmer-bg rounded-full w-1/5 mb-4" />
                <div className="h-8 shimmer-bg rounded-lg w-3/4 mb-6" />
                <div className="space-y-3">
                    {[...Array(6)].map((_, i) => <div key={i} className="h-4 shimmer-bg rounded-full" />)}
                </div>
            </div>
        );
    }

    if (error || !article) {
        return (
            <div className="text-center py-24">
                <p className="text-red-400 font-medium text-lg mb-6">{error ?? 'Article not found.'}</p>
                <button
                    onClick={() => navigate('/')}
                    className="px-6 py-2 bg-gradient-to-r from-sky-500 to-emerald-500 text-white font-semibold rounded-full hover:opacity-90 transition-opacity"
                >
                    Back to Home
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
                className="flex items-center gap-2 text-sky-400 hover:text-sky-300 font-semibold mb-6 transition-colors group"
            >
                <ArrowLeft className="w-4 h-4 transition-transform group-hover:-translate-x-1" strokeWidth={2} />
                Back
            </button>

            {/* Hero Image */}
            {article.image_url ? (
                <div className="rounded-2xl overflow-hidden mb-8 h-64 sm:h-96">
                    <img src={article.image_url} alt={article.title} className="w-full h-full object-cover" />
                </div>
            ) : (
                <div className="relative rounded-2xl overflow-hidden mb-8 h-64 flex items-center justify-center bg-gradient-to-br from-sky-900 via-cyan-900 to-emerald-900">
                    <div className="absolute inset-0 opacity-10"
                        style={{ backgroundImage: 'radial-gradient(circle, rgba(14,165,233,0.5) 1px, transparent 1px)', backgroundSize: '28px 28px' }} />
                    <span className="relative text-8xl opacity-70">{article.category?.emoji ?? ''}</span>
                </div>
            )}

            {/* Meta badges */}
            <div className="flex flex-wrap items-center gap-3 mb-4">
                {article.category && (
                    <span className="inline-flex items-center gap-1.5 text-sm font-semibold px-3 py-1 rounded-full bg-sky-500/15 text-sky-300 border border-sky-500/20">
                        {article.category.emoji} {article.category.name}
                    </span>
                )}
                {article.is_featured && (
                    <span className="inline-flex items-center gap-1.5 bg-gradient-to-r from-sky-500 to-emerald-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                        <Star className="w-3 h-3 fill-white" strokeWidth={0} />
                        Featured
                    </span>
                )}
            </div>

            {/* Title */}
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white leading-tight mb-4">
                {article.title}
            </h1>

            {/* Author / Source / Date */}
            <div className="flex flex-wrap items-center gap-5 text-sm text-slate-500 mb-8 pb-6 border-b border-white/[0.08]">
                {article.author && (
                    <span className="flex items-center gap-1.5 text-slate-400">
                        <Pen className="w-3.5 h-3.5 text-sky-500/70" strokeWidth={1.5} />
                        {article.author}
                    </span>
                )}
                {article.source && (
                    <span className="flex items-center gap-1.5">
                        <Newspaper className="w-3.5 h-3.5 text-sky-500/70" strokeWidth={1.5} />
                        {article.source}
                    </span>
                )}
                {article.published_at && (
                    <span className="flex items-center gap-1.5">
                        <Calendar className="w-3.5 h-3.5 text-sky-500/70" strokeWidth={1.5} />
                        {formatDate(article.published_at)}
                    </span>
                )}
            </div>

            {/* Content */}
            <div className="mb-12">
                {paragraphs.map((para, idx) => (
                    <p key={idx} className="text-slate-300 leading-relaxed text-lg mb-5">
                        {para?.trim()}
                    </p>
                ))}
            </div>

            {/* Save Button */}
            <div className="flex justify-end">
                <button
                    onClick={handleSave}
                    disabled={saving}
                    className={`flex items-center gap-2.5 px-6 py-3 rounded-full font-semibold text-sm transition-all duration-200
                        hover:scale-105 active:scale-95
                        ${article.is_saved
                            ? 'bg-gradient-to-r from-sky-500 to-emerald-500 text-white shadow-lg shadow-sky-500/30'
                            : 'bg-white/5 border border-white/10 text-slate-300 hover:border-sky-500/40 hover:bg-sky-500/10 hover:text-sky-300'
                        }
                        ${saving ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                    <Bookmark
                        className="w-4 h-4"
                        strokeWidth={1.5}
                        fill={article.is_saved ? 'currentColor' : 'none'}
                    />
                    {article.is_saved ? 'Saved' : 'Save Story'}
                </button>
            </div>
        </div>
    );
};

export default ArticlePage;
