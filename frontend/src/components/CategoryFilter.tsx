import React from 'react';
import type { Category } from '../types';

interface CategoryFilterProps {
    categories: Category[];
    selected: string | null;
    onSelect: (name: string | null) => void;
}

const CategoryFilter: React.FC<CategoryFilterProps> = ({ categories, selected, onSelect }) => {
    return (
        <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
            {/* "All" pill */}
            <button
                onClick={() => onSelect(null)}
                className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 whitespace-nowrap
                    ${selected === null
                        ? 'bg-gradient-to-r from-sky-500 to-emerald-500 text-white shadow-lg shadow-sky-500/25 scale-105'
                        : 'bg-white/5 border border-white/10 text-slate-400 hover:border-sky-500/40 hover:bg-sky-500/10 hover:text-slate-200'
                    }`}
            >
                All Stories
            </button>

            {categories.map((cat) => (
                <button
                    key={cat.id}
                    onClick={() => onSelect(cat.name)}
                    className={`flex-shrink-0 flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 whitespace-nowrap
                        ${selected === cat.name
                            ? 'bg-gradient-to-r from-sky-500 to-emerald-500 text-white shadow-lg shadow-sky-500/25 scale-105'
                            : 'bg-white/5 border border-white/10 text-slate-400 hover:border-sky-500/40 hover:bg-sky-500/10 hover:text-slate-200'
                        }`}
                >
                    {/* Keep category emoji — it's meaningful content branding */}
                    <span className="text-sm">{cat.emoji}</span>
                    <span>{cat.name}</span>
                </button>
            ))}
        </div>
    );
};

export default CategoryFilter;
