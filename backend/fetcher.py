"""
fetcher.py — Async news fetcher using NewsAPI.org, Reddit, and RSS feeds.

Searches for all kinds of uplifting, positive news per category and stores
new articles in the DB. De-duplicates by URL so re-runs are safe.
"""
import logging
import re
import asyncio
import time
from datetime import datetime, timezone

import httpx
import feedparser
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import AsyncSessionLocal
from models import Article, Category

logger = logging.getLogger(__name__)

NEWSAPI_BASE = "https://newsapi.org/v2/everything"

# ── Per-category query lists ──────────────────────────────────────────────────
CATEGORY_QUERIES: dict[str, list[str]] = {
    "Science": [
        "scientific breakthrough discovery",
        "medical milestone cure treatment success",
        "space exploration mission success",
        "climate solution research innovation",
        "new study finds benefit health",
        "scientists develop invent create solution",
        "research progress advance promising",
        "gene therapy trial success patients",
        "NASA discovery planet universe",
    ],
    "Environment": [
        "conservation success wildlife recovery",
        "renewable energy solar wind record",
        "reforestation rewilding habitat restored",
        "ocean cleanup plastic pollution solution",
        "endangered species saved protected",
        "green energy transition milestone",
        "national park protected nature reserve",
        "coral reef recovery restored ocean",
        "electric vehicles adoption growth",
        "zero emissions carbon neutral achievement",
    ],
    "Community": [
        "community hero volunteer kind act",
        "neighborhood initiative grassroots success",
        "charity fundraiser milestone impact",
        "local hero rescued helped saved lives",
        "town village celebrates achievement milestone",
        "random act of kindness community",
        "donation fundraising record goal reached",
        "students youth award recognition",
        "nonprofit impact community program success",
        "family reunited heartwarming story",
    ],
    "Health": [
        "health breakthrough therapy wellbeing",
        "mental health support awareness success",
        "hospital patient recovery miracle story",
        "public health improvement life expectancy",
        "disability accessibility achievement",
        "new treatment approved FDA patients",
        "vaccine success disease eradicated",
        "longevity anti-aging research breakthrough",
        "exercise wellness study benefit",
        "rare disease cure hope patients",
    ],
    "Animals": [
        "animal rescue sanctuary saved adopted",
        "wildlife conservation species recovery",
        "dog cat pet heartwarming reunited",
        "zoo breeding program endangered",
        "ocean marine life reef recovery",
        "wolf bear eagle population recovery",
        "shelter adoption record animals saved",
        "dolphin whale rescued released ocean",
        "birds migration habitat protected",
    ],
    "Technology": [
        "technology innovation helps people",
        "accessibility assistive tech disability",
        "clean tech green solution energy",
        "AI machine learning positive benefit",
        "startup nonprofit tech social good",
        "app platform helps community",
        "robotics prosthetic limb disability",
        "open source project benefit millions",
        "tech education coding youth empowerment",
        "medical device innovation saves lives",
    ],
    "Arts & Culture": [
        "art culture award celebration achievement",
        "museum exhibit festival community",
        "music concert film book celebrated",
        "cultural heritage preserved restored",
        "young artist student creative award",
        "indigenous culture language revival",
        "mural public art community project",
        "literary prize award author celebrated",
        "dance theater performance landmark",
    ],
}

POSITIVE_SIGNALS = {
    "breakthrough", "milestone", "success", "hope", "inspir", "celebrat",
    "achiev", "award", "rescue", "recover", "restor", "save", "hero",
    "volunteer", "kind", "heartwarming", "amazing", "record", "first ever",
    "historic", "triumph", "victory", "positive", "improve", "empower",
    "community", "together", "reunite", "grateful", "joy", "smile",
}

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


async def _fetch_newsapi(client: httpx.AsyncClient, api_key: str, categories: dict[str, int]) -> list[dict]:
    if not api_key or api_key == "your_newsapi_key_here":
        logger.warning("NEWS_API_KEY not configured — skipping NewsAPI fetch")
        return []

    articles = []
    seen = set()
    for cat_name, queries in CATEGORY_QUERIES.items():
        cat_id = categories.get(cat_name)
        if not cat_id:
            continue
        for query in queries:
            try:
                resp = await client.get(
                    NEWSAPI_BASE,
                    params={
                        "q": query,
                        "language": "en",
                        "sortBy": "publishedAt",
                        "pageSize": 20,
                        "apiKey": api_key,
                    },
                    timeout=15.0,
                )
                resp.raise_for_status()
                data = resp.json()
                if data.get("status") == "ok":
                    for raw in data.get("articles", []):
                        url = (raw.get("url") or "").strip()
                        if url and url not in seen and raw.get("urlToImage") and _is_positive(raw):
                            seen.add(url)
                            raw["_cat_id"] = cat_id
                            articles.append(raw)
                else:
                    logger.warning(f"NewsAPI non-ok status for '{query}': {data.get('message')}")
            except Exception as e:
                logger.error(f"NewsAPI error for '{query}': {e}")
    return articles


async def _fetch_reddit(client: httpx.AsyncClient, categories: dict[str, int]) -> list[dict]:
    subreddits = {
        "UpliftingNews": "Community",
        "MadeMeSmile": "Community",
        "PupliftingNews": "Animals",
        "happy": "Community",
        "goodnews": "Community",
        "WholesomeNews": "Community",
        "HumansBeingBros": "Community",
        "Positivity": "Health",
        "uplifting": "Community",
        "Eyebleach": "Animals",
        "Futurology": "Technology",
        "science": "Science",
        "environment": "Environment",
        "worldnews": "Community",
        "todayilearned": "Community",
        "mildlyinteresting": "Community",
        "interestingasfuck": "Community",
        "NatureIsFuckingLit": "Animals",
        "aww": "Animals",
        "ConservationSuccess": "Environment",
        "ClimateActionPlan": "Environment",
        "SolarPunk": "Environment",
        "EarthPorn": "Environment",
        "spaceporn": "Science",
        "space": "Science",
    }
    
    articles = []
    seen = set()
    for sub, cat_name in subreddits.items():
        cat_id = categories.get(cat_name) or categories.get("Community")
        if not cat_id:
            continue
            
        try:
            resp = await client.get(
                f"https://www.reddit.com/r/{sub}/hot.json?limit=25",
                headers={"User-Agent": "PositiveNewsApp/1.0"},
                timeout=15.0
            )
            resp.raise_for_status()
            data = resp.json()
            for child in data.get("data", {}).get("children", []):
                post = child.get("data", {})
                if post.get("is_self") or post.get("over_18") or post.get("stickied"):
                    continue
                    
                url = post.get("url", "").strip()
                if not url or url.startswith("https://www.reddit.com") or url in seen:
                    continue
                    
                title = post.get("title", "")
                
                # Image extraction
                image_url = ""
                preview = post.get("preview", {})
                if preview.get("images"):
                    image_url = preview["images"][0]["source"]["url"].replace("&amp;", "&")
                    
                raw = {
                    "title": title,
                    "description": title, # text posts are excluded, so title is best
                    "url": url,
                    "urlToImage": image_url,
                    "source": {"name": f"Reddit (r/{sub})"},
                    "author": post.get("author", ""),
                    "publishedAt": datetime.fromtimestamp(post.get("created_utc", 0), tz=timezone.utc).isoformat()
                }
                
                if _is_positive(raw):
                    seen.add(url)
                    raw["_cat_id"] = cat_id
                    articles.append(raw)
        except Exception as e:
            logger.error(f"Reddit error for r/{sub}: {e}")
            
    return articles


def _parse_feed_sync(url: str):
    return feedparser.parse(url)


async def _fetch_rss(categories: dict[str, int]) -> list[dict]:
    feeds = [
        # Dedicated positive/good news
        "https://www.goodnewsnetwork.org/feed/",
        "https://www.positive.news/feed/",
        "https://www.optimistdaily.com/feed/",
        "https://reasonstobecheerful.world/feed/",
        "https://www.sunnyskyz.com/rss.php",
        "https://www.upworthy.com/feeds/feed.rss",
        "https://www.goodgoodgood.co/rss",
        "https://www.shareable.net/feed/",
        "https://yesmagazine.org/feed/",
        "https://globaloptimism.com/feed/",
        "https://thecorrespondent.com/feed/rss",
        "https://futurecrunch.com/feed/",
        # Science & environment
        "https://www.sciencedaily.com/rss/top/science.xml",
        "https://feeds.nationalgeographic.com/ng/News/News_Main",
        "https://www.treehugger.com/feeds/all",
        "https://inhabitat.com/feed/",
        "https://cleantechnica.com/feed/",
        "https://www.renewableenergyworld.com/feed/",
        # Health & wellness
        "https://www.health.com/feeds/all",
        "https://greatergood.berkeley.edu/feeds/articles",
        # Community & culture
        "https://www.globalcitizen.org/en/feed/",
        "https://nextcity.org/feed",
        "https://civicnation.org/feed/",
    ]
    
    articles = []
    seen = set()
    
    cat_words = {name.lower(): cat_id for name, cat_id in categories.items()}
    default_cat_id = categories.get("Community")
    
    for feed_url in feeds:
        try:
            parsed = await asyncio.to_thread(_parse_feed_sync, feed_url)
            source_name = getattr(parsed.feed, "title", "RSS Feed")

            for entry in parsed.entries[:50]:  # raised from 25 → 50
                url = getattr(entry, "link", "").strip()
                if not url or url in seen:
                    continue
                    
                title = getattr(entry, "title", "")
                
                # feedparser adds an array of dictionaries for description content
                description = ""
                if hasattr(entry, "description"):
                    description = entry.description
                elif hasattr(entry, "summary"):
                    description = entry.summary
                
                # Try to get image — check all common RSS image locations
                image_url = ""
                if hasattr(entry, "media_content") and entry.media_content:
                    image_url = entry.media_content[0].get("url", "")
                if not image_url and hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
                    image_url = entry.media_thumbnail[0].get("url", "")
                if not image_url and hasattr(entry, "links"):
                    for link in entry.links:
                        lt = link.get("type", "")
                        if lt.startswith("image/") or link.get("rel") == "enclosure":
                            image_url = link.get("href", "")
                            break
                # Last resort: parse first <img> from the HTML description
                if not image_url and description:
                    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', description)
                    if m:
                        image_url = m.group(1)
                            
                published_at_str = ""
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published_at_str = datetime.fromtimestamp(time.mktime(entry.published_parsed), tz=timezone.utc).isoformat()
                    
                raw = {
                    "title": title,
                    "description": description[:500],
                    "url": url,
                    "urlToImage": image_url,
                    "source": {"name": source_name},
                    "author": getattr(entry, "author", ""),
                    "publishedAt": published_at_str
                }
                
                if _is_positive(raw):
                    seen.add(url)

                    # Guess category from title + description text
                    text = (title + " " + description).lower()
                    assigned_cat_id = default_cat_id
                    for word, cat_id in cat_words.items():
                        if word in text:
                            assigned_cat_id = cat_id
                            break

                    raw["_cat_id"] = assigned_cat_id
                    articles.append(raw)
        except Exception as e:
            logger.error(f"RSS error for {feed_url}: {e}")
            
    return articles


async def fetch_and_store_news(api_key: str) -> dict:
    """
    Fetch all categories, filter for positive stories, store new articles.
    Returns: {fetched, skipped, errors}
    """
    fetched = 0
    skipped = 0
    errors: list[str] = []

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Category))
        categories = {c.name: c.id for c in result.scalars().all()}
        
        if not categories:
            msg = "No categories in DB — run seed.py first"
            logger.warning(msg)
            return {"fetched": 0, "skipped": 0, "errors": [msg]}

        url_result = await db.execute(select(Article.url).where(Article.url.isnot(None)))
        existing_urls: set[str] = set(url_result.scalars().all())

        # Fetch from all sources concurrently
        async with httpx.AsyncClient() as client:
            newsapi_task = _fetch_newsapi(client, api_key, categories)
            reddit_task = _fetch_reddit(client, categories)
            rss_task = _fetch_rss(categories)
            
            results = await asyncio.gather(newsapi_task, reddit_task, rss_task, return_exceptions=True)
            
        all_articles = []
        for res in results:
            if isinstance(res, list):
                all_articles.extend(res)
            elif isinstance(res, Exception):
                logger.error(f"Fetcher task failed: {res}")
                errors.append(str(res))

        for raw in all_articles:
            url = (raw.get("url") or "").strip()[:1000]
            if not url or url in existing_urls:
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
            )[:5000]

            article = Article(
                title=(raw.get("title") or "Untitled")[:500],
                summary=summary,
                content=content,
                image_url=(raw.get("urlToImage") or "")[:1000],
                url=url,
                source=source_name[:200],
                author=(raw.get("author") or "")[:200],
                published_at=pub_at,
                category_id=raw.get("_cat_id"),
                is_featured=False,
                is_saved=False,
            )
            db.add(article)

            try:
                await db.flush()
                existing_urls.add(url)
                fetched += 1
            except IntegrityError:
                await db.rollback()
                skipped += 1

        await db.commit()

    logger.info(f"✅ News fetch done — {fetched} new, {skipped} skipped")
    return {"fetched": fetched, "skipped": skipped, "errors": errors}
