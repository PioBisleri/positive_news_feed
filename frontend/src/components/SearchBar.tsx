import React from 'react';
import { Search, X } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';

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
        debounceRef.current = setTimeout(() => onSearch(query), 300);
    };

    const handleClear = () => { setValue(''); onSearch(''); };

    useEffect(() => () => { if (debounceRef.current) clearTimeout(debounceRef.current); }, []);

    return (
        <div className="relative w-full max-w-xl mx-auto group">
            {/* Glow border */}
            <div className="absolute -inset-0.5 rounded-2xl bg-gradient-to-r from-sky-500 to-emerald-500 opacity-0 group-focus-within:opacity-40 blur transition-opacity duration-300" />

            <div className="relative flex items-center">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" strokeWidth={2} />

                <input
                    type="text"
                    value={value}
                    onChange={handleChange}
                    placeholder={placeholder}
                    className="relative w-full pl-11 pr-11 py-3.5 rounded-2xl
                        border border-white/15 text-white placeholder-slate-500 text-sm font-medium
                        focus:outline-none focus:ring-2 focus:ring-sky-500/50 focus:border-sky-500/60
                        transition-all duration-200"
                    style={{ background: 'rgba(255,255,255,0.07)' }}
                />

                {value && (
                    <button
                        onClick={handleClear}
                        className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
                        aria-label="Clear search"
                    >
                        <X className="w-4 h-4" strokeWidth={2} />
                    </button>
                )}
            </div>
        </div>
    );
};

export default SearchBar;
