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
                        ? 'bg-amber-500 text-white shadow-md scale-105'
                        : 'bg-white text-gray-600 border border-gray-200 hover:border-amber-300 hover:bg-amber-50'
                    }`}
            >
                🌍 All Stories
            </button>

            {categories.map((cat) => (
                <button
                    key={cat.id}
                    onClick={() => onSelect(cat.name)}
                    className={`flex-shrink-0 flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 whitespace-nowrap
            ${selected === cat.name
                            ? 'bg-amber-500 text-white shadow-md scale-105'
                            : 'bg-white text-gray-600 border border-gray-200 hover:border-amber-300 hover:bg-amber-50'
                        }`}
                >
                    <span>{cat.emoji}</span>
                    <span>{cat.name}</span>
                </button>
            ))}
        </div>
    );
};

export default CategoryFilter;
