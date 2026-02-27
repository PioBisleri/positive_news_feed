import React from 'react';
import { useNavigate } from 'react-router-dom';
import type { Article } from '../types';
import ReactionBar from './ReactionBar';
import { toggleSave } from '../api/client';

interface NewsCardProps {
    article: Article;
    onSaveToggle: (id: number, saved: boolean) => void;
    featured?: boolean;
}

const formatRelativeDate = (dateStr: string | null): string => {
    if (!dateStr) return '';
    const diff = (Date.now() - new Date(dateStr).getTime()) / 1000;
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
    return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

const getCategoryStyles = (color: string | null): string => {
    return color ?? 'bg-amber-100 text-amber-800';
};

const NewsCard: React.FC<NewsCardProps> = ({ article, onSaveToggle, featured = false }) => {
    const navigate = useNavigate();
    const [saving, setSaving] = React.useState(false);

    const handleCardClick = () => {
        navigate(`/article/${article.id}`);
    };

    const handleSave = async (e: React.MouseEvent) => {
        e.stopPropagation();
        if (saving) return;
        setSaving(true);
        try {
            const updated = await toggleSave(article.id);
            onSaveToggle(article.id, updated.is_saved);
        } catch {
            // ignore
        } finally {
            setSaving(false);
        }
    };

    const imageSrc = article.image_url ?? null;

    return (
        <article
            onClick={handleCardClick}
            className={`group bg-white rounded-2xl overflow-hidden shadow-card hover:shadow-card-hover
        cursor-pointer transition-all duration-300 hover:-translate-y-1 animate-fade-in flex flex-col
        ${featured ? 'md:flex-row' : ''}`}
        >
            {/* Image */}
            <div
                className={`relative overflow-hidden flex-shrink-0
          ${featured ? 'md:w-1/2 h-56 md:h-auto' : 'h-48'}`}
            >
                {imageSrc ? (
                    <img
                        src={imageSrc}
                        alt={article.title}
                        loading="lazy"
                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                    />
                ) : (
                    <div className="w-full h-full bg-gradient-to-br from-amber-200 via-orange-100 to-yellow-200 flex items-center justify-center">
                        <span className="text-5xl opacity-60">
                            {article.category?.emoji ?? '📰'}
                        </span>
                    </div>
                )}

                {/* Featured badge */}
                {article.is_featured && (
                    <span className="absolute top-3 left-3 bg-amber-500 text-white text-xs font-bold px-2.5 py-1 rounded-full shadow">
                        ⭐ Featured
                    </span>
                )}
            </div>

            {/* Content */}
            <div className={`flex flex-col flex-1 p-5 ${featured ? 'justify-between' : ''}`}>
                <div>
                    {/* Category badge */}
                    {article.category && (
                        <span
                            className={`inline-block text-xs font-semibold px-2.5 py-1 rounded-full mb-3 ${getCategoryStyles(article.category.color)}`}
                        >
                            {article.category.emoji} {article.category.name}
                        </span>
                    )}

                    {/* Title */}
                    <h2
                        className={`font-bold text-gray-900 mb-2 leading-snug group-hover:text-amber-700 transition-colors
              ${featured ? 'text-2xl' : 'text-lg'}`}
                    >
                        {article.title}
                    </h2>

                    {/* Summary */}
                    <p className="text-gray-500 text-sm leading-relaxed line-clamp-3 mb-4">
                        {article.summary}
                    </p>
                </div>

                {/* Footer */}
                <div>
                    {/* Source + Date */}
                    <div className="flex items-center justify-between text-xs text-gray-400 mb-3">
                        <span className="font-medium text-gray-500 truncate max-w-[60%]">
                            {article.source}
                        </span>
                        <span>{formatRelativeDate(article.published_at)}</span>
                    </div>

                    {/* Reaction bar + Save */}
                    <div className="flex items-center justify-between gap-2">
                        <div className="flex-1 min-w-0">
                            <ReactionBar articleId={article.id} reactions={article.reactions} size="sm" />
                        </div>

                        {/* Bookmark button */}
                        <button
                            onClick={handleSave}
                            disabled={saving}
                            title={article.is_saved ? 'Remove from saved' : 'Save article'}
                            className={`flex-shrink-0 text-xl transition-all duration-200 hover:scale-125 active:scale-95
                ${saving ? 'opacity-50' : ''}
                ${article.is_saved ? 'opacity-100' : 'opacity-40 hover:opacity-70'}`}
                        >
                            {article.is_saved ? '🔖' : '🔖'}
                        </button>
                    </div>
                </div>
            </div>
        </article>
    );
};

export default NewsCard;
