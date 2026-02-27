import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar: React.FC = () => {
    const location = useLocation();

    const isActive = (path: string) =>
        location.pathname === path
            ? 'text-amber-700 font-semibold border-b-2 border-amber-500'
            : 'text-amber-900 hover:text-amber-600 font-medium transition-colors';

    return (
        <nav className="sticky top-0 z-50 bg-gradient-to-r from-amber-400 via-orange-300 to-yellow-300 shadow-md">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-2 group">
                        <span className="text-2xl transition-transform group-hover:scale-110 duration-200">☀️</span>
                        <span className="text-xl font-extrabold text-amber-900 tracking-tight">
                            BrightFeed
                        </span>
                    </Link>

                    {/* Nav Links */}
                    <div className="flex items-center gap-6">
                        <Link to="/" className={`${isActive('/')} pb-0.5`}>
                            Home
                        </Link>
                        <Link to="/saved" className={`${isActive('/saved')} pb-0.5`}>
                            ✨ Saved
                        </Link>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
