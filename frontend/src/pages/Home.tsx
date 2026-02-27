import React, { useState, useEffect, useCallback } from 'react';
import type { Article, ArticleFilters, Category } from '../types';
import { fetchArticles, fetchCategories } from '../api/client';
import CategoryFilter from '../components/CategoryFilter';
import SearchBar from '../components/SearchBar';
import NewsCard from '../components/NewsCard';

const SkeletonCard: React.FC = () => (
    <div className="bg-white rounded-2xl overflow-hidden shadow-card animate-pulse">
        <div className="h-48 bg-amber-100" />
        <div className="p-5 space-y-3">
            <div className="h-3 bg-amber-100 rounded w-1/4" />
            <div className="h-5 bg-gray-200 rounded w-3/4" />
            <div className="h-3 bg-gray-100 rounded" />
            <div className="h-3 bg-gray-100 rounded w-5/6" />
            <div className="flex gap-2 mt-4">
                {[...Array(4)].map((_, i) => (
                    <div key={i} className="h-7 w-14 bg-amber-100 rounded-full" />
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
            setError('Oops! Could not load stories. Make sure the backend is running.');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchCategories()
            .then(setCategories)
            .catch(() => { });
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
        setArticles((prev) =>
            prev.map((a) => (a.id === id ? { ...a, is_saved: saved } : a))
        );
    };

    const featured = articles.filter((a) => a.is_featured);
    const regular = articles.filter((a) => !a.is_featured);

    return (
        <div>
            {/* Hero Section */}
            <div className="bg-gradient-to-br from-amber-400 via-orange-300 to-yellow-200 py-16 px-4">
                <div className="max-w-3xl mx-auto text-center">
                    <h1 className="text-4xl sm:text-5xl font-extrabold text-amber-900 mb-4 leading-tight">
                        The World Has Good News ✨
                    </h1>
                    <p className="text-amber-800 text-lg sm:text-xl font-medium mb-8 opacity-90">
                        Discover uplifting stories that remind you humanity is moving forward.
                        Science, nature, community, and more — all positive, all real.
                    </p>
                    <SearchBar onSearch={handleSearch} />
                </div>
            </div>

            {/* Main Content */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
                {/* Category Filter */}
                <div className="mb-8">
                    <CategoryFilter
                        categories={categories}
                        selected={filters.category ?? null}
                        onSelect={handleCategorySelect}
                    />
                </div>

                {/* Error State */}
                {error && (
                    <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-6 mb-8 text-center">
                        <span className="text-3xl block mb-2">😕</span>
                        <p className="font-medium">{error}</p>
                    </div>
                )}

                {/* Loading State */}
                {loading ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {[...Array(6)].map((_, i) => <SkeletonCard key={i} />)}
                    </div>
                ) : (
                    <>
                        {/* Featured Articles */}
                        {featured.length > 0 && (
                            <div className="mb-10">
                                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                                    ⭐ <span>Featured Stories</span>
                                </h2>
                                <div className="space-y-6">
                                    {featured.map((article) => (
                                        <NewsCard
                                            key={article.id}
                                            article={article}
                                            onSaveToggle={handleSaveToggle}
                                            featured
                                        />
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Regular Articles Grid */}
                        {regular.length > 0 ? (
                            <div>
                                {featured.length > 0 && (
                                    <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                                        📰 <span>More Uplifting Stories</span>
                                    </h2>
                                )}
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {regular.map((article) => (
                                        <NewsCard
                                            key={article.id}
                                            article={article}
                                            onSaveToggle={handleSaveToggle}
                                        />
                                    ))}
                                </div>
                            </div>
                        ) : articles.length === 0 && !loading ? (
                            <div className="text-center py-20 animate-fade-in">
                                <span className="text-7xl block mb-4">🌤️</span>
                                <h2 className="text-2xl font-bold text-gray-700 mb-2">No stories found</h2>
                                <p className="text-gray-500">Try a different search or category.</p>
                            </div>
                        ) : null}
                    </>
                )}
            </div>
        </div>
    );
};

export default Home;
