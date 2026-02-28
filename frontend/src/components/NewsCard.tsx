import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Bookmark, Star } from 'lucide-react';
import type { Article } from '../types';
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

const NewsCard: React.FC<NewsCardProps> = ({ article, onSaveToggle, featured = false }) => {
    const navigate = useNavigate();
    const [saving, setSaving] = React.useState(false);

    const handleCardClick = () => navigate(`/article/${article.id}`);

    const handleSave = async (e: React.MouseEvent) => {
        e.stopPropagation();
        if (saving) return;
        setSaving(true);
        try {
            const updated = await toggleSave(article.id);
            onSaveToggle(article.id, updated.is_saved);
        } catch { /* ignore */ }
        finally { setSaving(false); }
    };

    const imageSrc = article.image_url ?? null;

    return (
        <article
            onClick={handleCardClick}
            className={`group flex flex-col cursor-pointer animate-fade-in
                bg-white/[0.03] border border-white/[0.08] backdrop-blur-xl rounded-2xl overflow-hidden
                transition-all duration-300 hover:-translate-y-1 hover:bg-white/[0.06]
                hover:border-sky-500/30 hover:shadow-[0_8px_32px_rgba(14,165,233,0.15)]
                ${featured ? 'md:flex-row md:min-h-[420px]' : ''}`}
        >
            {/* Image Section */}
            <div className={`relative overflow-hidden flex-shrink-0 ${featured ? 'md:w-[45%] h-64 md:h-full' : 'h-52'}`}>
                {imageSrc ? (
                    <img
                        src={imageSrc}
                        alt={article.title}
                        loading="lazy"
                        className="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105 brightness-90 group-hover:brightness-100"
                    />
                ) : (
                    <div className="w-full h-full bg-slate-900 flex items-center justify-center overflow-hidden">
                        {/* Abstract geometric fallback pattern */}
                        <div className="absolute inset-0 opacity-20"
                            style={{
                                backgroundImage: `
                                    radial-gradient(circle at 0% 0%, rgba(14,165,233,0.4) 0%, transparent 50%),
                                    radial-gradient(circle at 100% 100%, rgba(16,185,129,0.3) 0%, transparent 50%)
                                `
                            }}
                        />
                        <div className="absolute inset-0 opacity-10"
                            style={{ backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)', backgroundSize: '32px 32px' }}
                        />
                        {/* Subtle watermark logo instead of a giant emoji */}
                        <div className="w-16 h-16 rounded-full border border-sky-500/20 flex items-center justify-center opacity-30 shadow-[0_0_30px_rgba(14,165,233,0.2)]">
                            <span className="text-3xl opacity-50">{article.category?.emoji ?? '📰'}</span>
                        </div>
                    </div>
                )}

                {/* Floating Badges */}
                <div className="absolute top-3 left-3 flex flex-col gap-2 items-start">
                    {/* Featured badge */}
                    {article.is_featured && (
                        <span className="flex items-center gap-1.5 bg-gradient-to-r from-sky-500 to-emerald-500 text-white text-[11px] font-bold uppercase tracking-wider px-3 py-1.5 rounded-full shadow-lg backdrop-blur-md">
                            <Star className="w-3 h-3 fill-white" strokeWidth={0} />
                            Featured
                        </span>
                    )}

                    {/* Category badge moved UP over the image */}
                    {article.category && (
                        <span className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full bg-slate-900/80 text-white border border-white/10 backdrop-blur-md shadow-lg">
                            <span className="text-sm">{article.category.emoji}</span>
                            {article.category.name}
                        </span>
                    )}
                </div>

                {/* Bottom gradient fade for text contrast if text were over it, mostly stylistic here */}
                <div className="absolute inset-x-0 bottom-0 h-20 bg-gradient-to-t from-slate-950/80 to-transparent" />
            </div>

            {/* Content Section */}
            <div className={`flex flex-col flex-1 p-6 ${featured ? 'justify-between py-8 px-8' : ''}`}>
                <div className="flex-1">
                    {/* Title */}
                    <h2 className={`font-bold text-slate-100 mb-3 leading-snug group-hover:text-sky-300 transition-colors duration-300
                        ${featured ? 'text-3xl tracking-tight' : 'text-xl tracking-tight'}`}>
                        {article.title}
                    </h2>

                    {/* Summary - reduced to line-clamp-2 for cleaner uniform height */}
                    <p className={`text-slate-400 leading-relaxed line-clamp-2 ${featured ? 'text-base mb-6' : 'text-sm mb-4'}`}>
                        {article.summary}
                    </p>
                </div>

                {/* Footer (Source, Date, Save) - NO HARD BORDER */}
                <div className="flex items-center justify-between mt-auto pt-2">
                    <div className="flex items-center gap-3">
                        <span className="text-xs font-semibold text-sky-400 capitalize tracking-wide">
                            {article.source || 'News Source'}
                        </span>
                        <span className="w-1 h-1 rounded-full bg-slate-700" />
                        <span className="text-xs font-medium text-slate-500">
                            {formatRelativeDate(article.published_at)}
                        </span>
                    </div>

                    <button
                        onClick={handleSave}
                        disabled={saving}
                        title={article.is_saved ? 'Remove from saved' : 'Save article'}
                        className={`p-2 -mr-2 rounded-full transition-all duration-300 hover:bg-white/5 active:scale-90
                            ${saving ? 'opacity-50' : ''}
                            ${article.is_saved
                                ? 'text-emerald-400 drop-shadow-[0_0_8px_rgba(16,185,129,0.5)]'
                                : 'text-slate-500 hover:text-slate-300'}`}
                    >
                        <Bookmark
                            className="w-5 h-5 transition-transform group-hover:scale-110"
                            strokeWidth={1.5}
                            fill={article.is_saved ? 'currentColor' : 'none'}
                        />
                    </button>
                </div>
            </div>
        </article>
    );
};

export default NewsCard;
