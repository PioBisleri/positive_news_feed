import React, { useState } from 'react';
import type { Reaction, ReactionType } from '../types';
import { REACTION_META } from '../types';
import { addReaction } from '../api/client';

interface ReactionBarProps {
    articleId: number;
    reactions: Reaction[];
    size?: 'sm' | 'lg';
}

const ReactionBar: React.FC<ReactionBarProps> = ({ articleId, reactions, size = 'sm' }) => {
    const [localReactions, setLocalReactions] = useState<Reaction[]>(reactions);
    const [bouncing, setBouncing] = useState<string | null>(null);

    const getCount = (type: string): number => {
        return localReactions.find((r) => r.reaction_type === type)?.count ?? 0;
    };

    const handleReact = async (e: React.MouseEvent, type: ReactionType) => {
        e.stopPropagation();
        e.preventDefault();

        // Optimistic update
        setLocalReactions((prev) => {
            const existing = prev.find((r) => r.reaction_type === type);
            if (existing) {
                return prev.map((r) =>
                    r.reaction_type === type ? { ...r, count: r.count + 1 } : r
                );
            }
            return [
                ...prev,
                { id: Date.now(), article_id: articleId, reaction_type: type, count: 1 },
            ];
        });

        // Bounce animation
        setBouncing(type);
        setTimeout(() => setBouncing(null), 400);

        try {
            const updated = await addReaction(articleId, type);
            setLocalReactions((prev) =>
                prev.map((r) =>
                    r.reaction_type === type ? { ...r, count: updated.count } : r
                )
            );
        } catch {
            // Revert on error
            setLocalReactions(reactions);
        }
    };

    const btnSize = size === 'lg' ? 'px-4 py-2 text-base gap-2' : 'px-2.5 py-1.5 text-xs gap-1';
    const emojiSize = size === 'lg' ? 'text-xl' : 'text-sm';

    return (
        <div className="flex flex-wrap gap-2" onClick={(e) => e.stopPropagation()}>
            {(Object.entries(REACTION_META) as [ReactionType, { emoji: string; label: string }][]).map(
                ([type, meta]) => (
                    <button
                        key={type}
                        onClick={(e) => handleReact(e, type)}
                        title={meta.label}
                        className={`flex items-center ${btnSize} rounded-full bg-white border border-gray-200
              hover:border-amber-300 hover:bg-amber-50 font-medium text-gray-600
              transition-all duration-150 hover:scale-105
              ${bouncing === type ? 'scale-125 border-amber-400' : ''}
              active:scale-95`}
                    >
                        <span className={`${emojiSize} ${bouncing === type ? 'animate-bounce' : ''}`}>
                            {meta.emoji}
                        </span>
                        <span className="tabular-nums font-semibold text-amber-700">
                            {getCount(type).toLocaleString()}
                        </span>
                    </button>
                )
            )}
        </div>
    );
};

export default ReactionBar;
