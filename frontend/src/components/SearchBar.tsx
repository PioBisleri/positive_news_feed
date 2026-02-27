import React, { useState, useEffect, useRef } from 'react';

interface SearchBarProps {
    onSearch: (query: string) => void;
    placeholder?: string;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, placeholder = 'Search uplifting stories...' }) => {
    const [value, setValue] = useState('');
    const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const query = e.target.value;
        setValue(query);

        if (debounceRef.current) clearTimeout(debounceRef.current);
        debounceRef.current = setTimeout(() => {
            onSearch(query);
        }, 300);
    };

    const handleClear = () => {
        setValue('');
        onSearch('');
    };

    useEffect(() => {
        return () => {
            if (debounceRef.current) clearTimeout(debounceRef.current);
        };
    }, []);

    return (
        <div className="relative w-full max-w-xl mx-auto">
            {/* Search icon */}
            <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none select-none text-lg">
                🔍
            </span>

            <input
                type="text"
                value={value}
                onChange={handleChange}
                placeholder={placeholder}
                className="w-full pl-10 pr-10 py-3 rounded-2xl border border-gray-200 bg-white shadow-sm
          text-gray-800 placeholder-gray-400 text-sm font-medium
          focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400
          transition-all duration-200"
            />

            {value && (
                <button
                    onClick={handleClear}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                    aria-label="Clear search"
                >
                    ✕
                </button>
            )}
        </div>
    );
};

export default SearchBar;
