import React, { useState, useEffect } from 'react';
import { Bookmark } from 'lucide-react';
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
            setArticles((prev) => prev.filter((a) => a.id !== id));
        } else {
            setArticles((prev) => prev.map((a) => (a.id === id ? { ...a, is_saved: saved } : a)));
        }
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            {/* Page Header */}
            <div className="mb-10 flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 to-emerald-500 flex items-center justify-center shadow-lg shadow-sky-500/20">
                    <Bookmark className="w-5 h-5 text-white fill-white/30" strokeWidth={1.5} />
                </div>
                <div>
                    <h1 className="text-3xl font-extrabold text-white">Saved Stories</h1>
                    <p className="text-slate-500 text-sm">Your personal collection of uplifting reads.</p>
                </div>
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
