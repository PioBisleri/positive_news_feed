"""
fetcher.py — Async news fetcher using NewsAPI.org.

Searches for all kinds of uplifting, positive news per category and stores
new articles in the DB. De-duplicates by URL so re-runs are safe.
"""
import logging
from datetime import datetime, timezone

import httpx
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import AsyncSessionLocal
from models import Article, Category, Reaction

logger = logging.getLogger(__name__)

NEWSAPI_BASE = "https://newsapi.org/v2/everything"

# ── Per-category query lists ──────────────────────────────────────────────────
# Each category has multiple targeted queries. We run them all and de-duplicate
# by URL so a single article can't appear twice even if it matches two queries.
# Queries are deliberately broad — capturing breakthroughs AND everyday wins,
# community stories, celebrations, heroes, and more.

CATEGORY_QUERIES: dict[str, list[str]] = {
    "Science": [
        "scientific breakthrough discovery",
        "medical milestone cure treatment success",
        "space exploration mission success",
        "climate solution research innovation",
    ],
    "Environment": [
        "conservation success wildlife recovery",
        "renewable energy solar wind record",
        "reforestation rewilding habitat restored",
        "ocean cleanup plastic pollution solution",
        "endangered species saved protected",
    ],
    "Community": [
        "community hero volunteer kind act",
        "neighborhood initiative grassroots success",
        "charity fundraiser milestone impact",
        "local hero rescued helped saved lives",
        "town village celebrates achievement milestone",
        "random act of kindness community",
    ],
    "Health": [
        "health breakthrough therapy wellbeing",
        "mental health support awareness success",
        "hospital patient recovery miracle story",
        "public health improvement life expectancy",
        "disability accessibility achievement",
    ],
    "Animals": [
        "animal rescue sanctuary saved adopted",
        "wildlife conservation species recovery",
        "dog cat pet heartwarming reunited",
        "zoo breeding program endangered",
        "ocean marine life reef recovery",
    ],
    "Technology": [
        "technology innovation helps people",
        "accessibility assistive tech disability",
        "clean tech green solution energy",
        "AI machine learning positive benefit",
        "startup nonprofit tech social good",
    ],
    "Arts & Culture": [
        "art culture award celebration achievement",
        "museum exhibit festival community",
        "music concert film book celebrated",
        "cultural heritage preserved restored",
        "young artist student creative award",
    ],
}

REACTION_TYPES = ["inspiring", "heartwarming", "amazing", "hopeful"]

# Positive sentiment terms — any matching article is strongly preferred
POSITIVE_SIGNALS = {
    "breakthrough", "milestone", "success", "hope", "inspir", "celebrat",
    "achiev", "award", "rescue", "recover", "restor", "save", "hero",
    "volunteer", "kind", "heartwarming", "amazing", "record", "first ever",
    "historic", "triumph", "victory", "positive", "improve", "empower",
    "community", "together", "reunite", "grateful", "joy", "smile",
}

# Hard-reject terms — drop articles containing these
NEGATIVE_SIGNALS = {
    "dead", "killed", "murder", "attack", "war", "terror", "crash",
    "shooting", "arrested", "convicted", "scandal", "disaster", "fraud",
    "abuse", "crisis", "[removed]",
}


def _is_positive(article: dict) -> bool:
    """Light sentiment filter — drops clearly negative articles."""
    text = " ".join([
        (article.get("title") or ""),
        (article.get("description") or ""),
    ]).lower()

    if article.get("url", "").rstrip("/") == "https://removed.com":
        return False
    if article.get("title") == "[Removed]":
        return False

    for neg in NEGATIVE_SIGNALS:
        if neg in text:
            return False

    return True


async def _fetch_query(
    client: httpx.AsyncClient,
    api_key: str,
    query: str,
    page_size: int = 20,
) -> list[dict]:
    """Run one NewsAPI query and return raw article list."""
    try:
        resp = await client.get(
            NEWSAPI_BASE,
            params={
                "q": query,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": page_size,
                "apiKey": api_key,
            },
            timeout=15.0,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "ok":
            logger.warning(f"NewsAPI non-ok status for '{query}': {data.get('message')}")
            return []
        return [
            a for a in data.get("articles", [])
            if a.get("urlToImage") and a.get("url") and _is_positive(a)
        ]
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP {e.response.status_code} for query '{query}'")
        return []
    except Exception as e:
        logger.error(f"Error fetching '{query}': {e}")
        return []


async def fetch_and_store_news(api_key: str) -> dict:
    """
    Fetch all categories, filter for positive stories, store new articles.
    Returns: {fetched, skipped, errors}
    """
    if not api_key or api_key == "your_newsapi_key_here":
        msg = "NEWS_API_KEY not configured — skipping news fetch"
        logger.warning(msg)
        return {"fetched": 0, "skipped": 0, "errors": [msg]}

    fetched = 0
    skipped = 0
    errors: list[str] = []

    async with AsyncSessionLocal() as db:
        # Load category name → id mapping
        result = await db.execute(select(Category))
        categories: dict[str, int] = {c.name: c.id for c in result.scalars().all()}

        if not categories:
            msg = "No categories in DB — run seed.py first"
            logger.warning(msg)
            return {"fetched": 0, "skipped": 0, "errors": [msg]}

        # Load existing URLs to prevent duplicates
        url_result = await db.execute(
            select(Article.url).where(Article.url.isnot(None))
        )
        existing_urls: set[str] = set(url_result.scalars().all())

        async with httpx.AsyncClient() as client:
            for cat_name, queries in CATEGORY_QUERIES.items():
                cat_id = categories.get(cat_name)
                if not cat_id:
                    continue

                # Collect articles across all queries for this category, dedup by URL
                seen_this_category: set[str] = set()
                category_articles: list[dict] = []

                for query in queries:
                    raw = await _fetch_query(client, api_key, query)
                    for article in raw:
                        url = (article.get("url") or "").strip()
                        if url and url not in seen_this_category and url not in existing_urls:
                            seen_this_category.add(url)
                            category_articles.append(article)

                # Store new articles
                for raw in category_articles:
                    url = (raw.get("url") or "").strip()[:1000]
                    if not url:
                        continue

                    pub_str = raw.get("publishedAt", "")
                    try:
                        pub_at = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
                    except Exception:
                        pub_at = datetime.now(timezone.utc)

                    summary = (raw.get("description") or raw.get("title") or "")[:2000]
                    source_name = (raw.get("source") or {}).get("name") or ""
                    content = (
                        f"{raw.get('description') or ''}\n\n"
                        f"Read the full story at {source_name or 'the source'}: {url}"
                    )

                    article = Article(
                        title=(raw.get("title") or "Untitled")[:500],
                        summary=summary,
                        content=content,
                        image_url=(raw.get("urlToImage") or "")[:1000],
                        url=url,
                        source=source_name[:200],
                        author=(raw.get("author") or "")[:200],
                        published_at=pub_at,
                        category_id=cat_id,
                        is_featured=False,
                        is_saved=False,
                    )
                    db.add(article)

                    try:
                        await db.flush()
                        for rtype in REACTION_TYPES:
                            db.add(Reaction(
                                article_id=article.id,
                                reaction_type=rtype,
                                count=0,
                            ))
                        existing_urls.add(url)
                        fetched += 1
                    except IntegrityError:
                        await db.rollback()
                        skipped += 1

        await db.commit()

    logger.info(f"✅ News fetch done — {fetched} new, {skipped} skipped")
    return {"fetched": fetched, "skipped": skipped, "errors": errors}
