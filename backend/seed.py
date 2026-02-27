"""
Seed script — run directly: python seed.py

Creates the DB tables and seeds the 7 categories.
All articles come from the live news fetcher (fetcher.py / POST /api/fetch-news).
"""
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5432/positivenews"
)

CATEGORIES = [
    {"name": "Science",       "emoji": "🔬", "color": "bg-blue-100 text-blue-800"},
    {"name": "Environment",   "emoji": "🌿", "color": "bg-green-100 text-green-800"},
    {"name": "Community",     "emoji": "🤝", "color": "bg-purple-100 text-purple-800"},
    {"name": "Health",        "emoji": "💪", "color": "bg-red-100 text-red-800"},
    {"name": "Animals",       "emoji": "🐾", "color": "bg-yellow-100 text-yellow-800"},
    {"name": "Technology",    "emoji": "💡", "color": "bg-indigo-100 text-indigo-800"},
    {"name": "Arts & Culture","emoji": "🎨", "color": "bg-pink-100 text-pink-800"},
]


def run_seed():
    conn = psycopg.connect(DATABASE_URL)
    cur = conn.cursor()

    # ── Schema migration (safe to re-run) ─────────────────────────────────────
    cur.execute("""
        ALTER TABLE IF EXISTS articles
            ADD COLUMN IF NOT EXISTS url VARCHAR(1000) UNIQUE
    """)
    conn.commit()

    # ── Create tables ──────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id    SERIAL PRIMARY KEY,
            name  VARCHAR(100) UNIQUE NOT NULL,
            emoji VARCHAR(10),
            color VARCHAR(50)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id           SERIAL PRIMARY KEY,
            title        VARCHAR(500) NOT NULL,
            summary      TEXT NOT NULL,
            content      TEXT,
            image_url    VARCHAR(1000),
            url          VARCHAR(1000) UNIQUE,
            source       VARCHAR(200),
            author       VARCHAR(200),
            published_at TIMESTAMPTZ DEFAULT NOW(),
            category_id  INTEGER REFERENCES categories(id),
            is_featured  BOOLEAN DEFAULT FALSE,
            is_saved     BOOLEAN DEFAULT FALSE,
            created_at   TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reactions (
            id            SERIAL PRIMARY KEY,
            article_id    INTEGER REFERENCES articles(id) ON DELETE CASCADE,
            reaction_type VARCHAR(50) NOT NULL,
            count         INTEGER DEFAULT 0
        )
    """)
    conn.commit()

    # ── Seed categories ────────────────────────────────────────────────────────
    for cat in CATEGORIES:
        cur.execute(
            """
            INSERT INTO categories (name, emoji, color)
            VALUES (%s, %s, %s)
            ON CONFLICT (name) DO UPDATE
                SET emoji = EXCLUDED.emoji,
                    color = EXCLUDED.color
            """,
            (cat["name"], cat["emoji"], cat["color"]),
        )
    conn.commit()
    print(f"✅ Seeded {len(CATEGORIES)} categories")

    cur.close()
    conn.close()
    print("🌟 DB ready — run the backend and POST /api/fetch-news to pull live articles")


if __name__ == "__main__":
    run_seed()
