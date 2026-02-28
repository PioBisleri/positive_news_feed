import React, { useState, useEffect, useCallback } from 'react';
import { Sparkles, AlertCircle } from 'lucide-react';
import type { Article, ArticleFilters, Category } from '../types';
import { fetchArticles, fetchCategories } from '../api/client';
import CategoryFilter from '../components/CategoryFilter';
import SearchBar from '../components/SearchBar';
import NewsCard from '../components/NewsCard';

const SkeletonCard: React.FC = () => (
    <div className="glass rounded-2xl overflow-hidden">
        <div className="h-48 shimmer-bg" />
        <div className="p-5 space-y-3">
            <div className="h-3 shimmer-bg rounded-full w-1/4" />
            <div className="h-5 shimmer-bg rounded-lg w-3/4" />
            <div className="h-3 shimmer-bg rounded-full" />
            <div className="h-3 shimmer-bg rounded-full w-5/6" />
            <div className="flex gap-2 mt-4">
                {[...Array(3)].map((_, i) => (
                    <div key={i} className="h-7 w-16 shimmer-bg rounded-full" />
                ))}
            </div>
        </div>
    </div>
);

const Home: React.FC = () => {
    const [articles, setArticles] = useState<Article[]>([]);
    const [categories, setCategories] = useState<Category[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [filters, setFilters] = useState<ArticleFilters>({});

    const loadData = useCallback(async (currentFilters: ArticleFilters) => {
        setLoading(true);
        setError(null);
        try {
            const data = await fetchArticles(currentFilters);
            setArticles(data);
        } catch {
            setError('Could not load stories. Make sure the backend is running.');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchCategories().then(setCategories).catch(() => { });
        loadData({});
    }, [loadData]);

    const handleCategorySelect = (name: string | null) => {
        const newFilters: ArticleFilters = { ...filters, category: name ?? undefined };
        setFilters(newFilters);
        loadData(newFilters);
    };

    const handleSearch = (query: string) => {
        const newFilters: ArticleFilters = { ...filters, search: query || undefined };
        setFilters(newFilters);
        loadData(newFilters);
    };

    const handleSaveToggle = (id: number, saved: boolean) => {
        setArticles((prev) => prev.map((a) => (a.id === id ? { ...a, is_saved: saved } : a)));
    };

    const featured = articles.filter((a) => a.is_featured);
    const regular = articles.filter((a) => !a.is_featured);

    return (
        <div>
            {/* ── Hero Section ── */}
            <div className="relative overflow-hidden py-20 px-4">
                <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-sky-950/40 to-emerald-950/30" />
                <div className="absolute top-10 left-1/4 w-72 h-72 rounded-full bg-sky-500/10 blur-3xl animate-float pointer-events-none" />
                <div className="absolute bottom-0 right-1/4 w-96 h-96 rounded-full bg-emerald-500/10 blur-3xl animate-float pointer-events-none" style={{ animationDelay: '3s' }} />

                <div className="relative max-w-3xl mx-auto text-center z-10">
                    {/* Live badge */}
                    <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/5 border border-white/10 text-slate-300 text-xs font-medium mb-6 animate-fade-in">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                        Curated positive stories, refreshed daily
                    </div>

                    <h1 className="text-4xl sm:text-6xl font-extrabold leading-tight mb-6 animate-slide-up">
                        <span className="gradient-text">The World Has</span>
                        <br />
                        <span className="text-white">Good News</span>
                    </h1>

                    <p className="text-slate-400 text-lg sm:text-xl font-medium mb-10 max-w-2xl mx-auto leading-relaxed animate-slide-up">
                        Discover uplifting stories that remind you humanity is moving forward —
                        science, nature, community, and more.
                    </p>

                    <div className="animate-slide-up">
                        <SearchBar onSearch={handleSearch} />
                    </div>

                    {/* Stats row */}
                    <div className="flex justify-center gap-8 mt-10 animate-fade-in">
                        {[
                            { label: 'Stories Today', value: articles.length > 0 ? `${articles.length}+` : '—' },
                            { label: 'Always Free', value: '100%' },
                        ].map(({ label, value }) => (
                            <div key={label} className="text-center">
                                <div className="text-2xl font-extrabold gradient-text">{value}</div>
                                <div className="text-slate-500 text-xs mt-0.5">{label}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* ── Main Content ── */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

                <div className="flex items-center gap-4 mb-8">
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent" />
                    <CategoryFilter categories={categories} selected={filters.category ?? null} onSelect={handleCategorySelect} />
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent" />
                </div>

                {/* Error State */}
                {error && (
                    <div className="glass border border-red-500/20 text-red-300 rounded-2xl p-6 mb-8 flex items-center gap-3">
                        <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" strokeWidth={1.5} />
                        <p className="font-medium">{error}</p>
                    </div>
                )}

                {loading ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {[...Array(6)].map((_, i) => <SkeletonCard key={i} />)}
                    </div>
                ) : (
                    <>
                        {/* Featured Articles */}
                        {featured.length > 0 && (
                            <div className="mb-10">
                                <SectionHeading label="Featured Stories" />
                                <div className="space-y-6">
                                    {featured.map((article) => (
                                        <NewsCard key={article.id} article={article} onSaveToggle={handleSaveToggle} featured />
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Regular Articles Grid */}
                        {regular.length > 0 ? (
                            <div>
                                {featured.length > 0 && <SectionHeading label="More Uplifting Stories" />}
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {regular.map((article) => (
                                        <NewsCard key={article.id} article={article} onSaveToggle={handleSaveToggle} />
                                    ))}
                                </div>
                            </div>
                        ) : articles.length === 0 && !loading ? (
                            <div className="text-center py-24 animate-fade-in">
                                <div className="inline-flex w-16 h-16 rounded-2xl bg-white/5 border border-white/10 items-center justify-center mb-4">
                                    <Sparkles className="w-8 h-8 text-slate-500" strokeWidth={1.5} />
                                </div>
                                <h2 className="text-2xl font-bold text-slate-300 mb-2">No stories found</h2>
                                <p className="text-slate-500">Try a different search or category.</p>
                            </div>
                        ) : null}
                    </>
                )}
            </div>
        </div>
    );
};

const SectionHeading: React.FC<{ label: string }> = ({ label }) => (
    <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-5 flex items-center gap-3">
        <span className="flex-1 h-px bg-gradient-to-r from-sky-500/30 to-transparent" />
        {label}
        <span className="flex-1 h-px bg-gradient-to-l from-emerald-500/30 to-transparent" />
    </h2>
);

export default Home;
