import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Leaf, Home, Bookmark } from 'lucide-react';

const Navbar: React.FC = () => {
    const location = useLocation();
    const isActive = (path: string) => location.pathname === path;

    return (
        <nav
            className="sticky top-0 z-50 border-b border-white/[0.06]"
            style={{ background: 'rgba(15,23,42,0.85)', backdropFilter: 'blur(20px)', WebkitBackdropFilter: 'blur(20px)' }}
        >
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">

                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-2.5 group">
                        <div className="relative w-9 h-9 flex items-center justify-center">
                            <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-sky-500 to-emerald-500 opacity-20 group-hover:opacity-40 blur transition-opacity duration-300" />
                            <div className="relative w-9 h-9 rounded-xl bg-gradient-to-br from-sky-500 to-emerald-500 flex items-center justify-center shadow-lg">
                                <Leaf className="w-5 h-5 text-white" strokeWidth={2} />
                            </div>
                        </div>
                        <span className="text-xl font-extrabold tracking-tight gradient-text">
                            BrightFeed
                        </span>
                    </Link>

                    {/* Nav Links */}
                    <div className="flex items-center gap-1">
                        <Link
                            to="/"
                            className={`relative px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-2
                                ${isActive('/')
                                    ? 'text-sky-300 bg-sky-500/10'
                                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                                }`}
                        >
                            {isActive('/') && (
                                <span className="absolute bottom-0 left-1/2 -translate-x-1/2 w-4 h-0.5 rounded-full bg-gradient-to-r from-sky-400 to-emerald-400" />
                            )}
                            <Home className="w-4 h-4" strokeWidth={isActive('/') ? 2 : 1.5} />
                            Home
                        </Link>
                        <Link
                            to="/saved"
                            className={`relative px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-2
                                ${isActive('/saved')
                                    ? 'text-emerald-300 bg-emerald-500/10'
                                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                                }`}
                        >
                            {isActive('/saved') && (
                                <span className="absolute bottom-0 left-1/2 -translate-x-1/2 w-4 h-0.5 rounded-full bg-gradient-to-r from-sky-400 to-emerald-400" />
                            )}
                            <Bookmark className={`w-4 h-4 ${isActive('/saved') ? 'fill-emerald-400/30' : ''}`} strokeWidth={1.5} />
                            Saved
                        </Link>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
