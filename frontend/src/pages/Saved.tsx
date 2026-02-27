import React, { useState, useEffect } from 'react';
import type { Article } from '../types';
import { fetchSavedArticles } from '../api/client';
import SavedArticles from '../components/SavedArticles';

const Saved: React.FC = () => {
    const [articles, setArticles] = useState<Article[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchSavedArticles()
            .then(setArticles)
            .catch(() => setError('Could not load saved articles.'))
            .finally(() => setLoading(false));
    }, []);

    const handleSaveToggle = (id: number, saved: boolean) => {
        if (!saved) {
            // Remove from list when unsaved
            setArticles((prev) => prev.filter((a) => a.id !== id));
        } else {
            setArticles((prev) =>
                prev.map((a) => (a.id === id ? { ...a, is_saved: saved } : a))
            );
        }
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <div className="mb-8">
                <h1 className="text-3xl font-extrabold text-gray-900 mb-1">
                    🔖 Saved Stories
                </h1>
                <p className="text-gray-500">Your collection of uplifting reads.</p>
            </div>

            <SavedArticles
                articles={articles}
                loading={loading}
                error={error}
                onSaveToggle={handleSaveToggle}
            />
        </div>
    );
};

export default Saved;
