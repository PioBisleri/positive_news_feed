from contextlib import asynccontextmanager
import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import engine
from fetcher import fetch_and_store_news
from routers import articles, categories

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables, seed categories, start scheduler, and run first fetch."""
    import asyncio
    from database import engine
    from models import Base
    from seed import run_seed_async

    # Auto-create tables (safe — uses CREATE TABLE IF NOT EXISTS logic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("🗃️  Database tables ready")

    # Seed categories (idempotent)
    await run_seed_async()
    logger.info("🌱 Categories seeded")

    # Schedule news fetch every 6 hours
    scheduler.add_job(
        fetch_and_store_news,
        trigger=IntervalTrigger(hours=6),
        args=[settings.news_api_key],
        id="news_fetch",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("🕐 News fetch scheduler started (every 6 hours)")

    # Trigger an immediate fetch on startup (non-blocking)
    asyncio.create_task(fetch_and_store_news(settings.news_api_key))

    yield  # ── app is running ──

    scheduler.shutdown(wait=False)
    logger.info("🛑 Scheduler stopped")


app = FastAPI(
    title="BrightFeed API",
    description="Positive news feed — uplifting stories for a better day.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
# Set FRONTEND_URL env var on Render to your Vercel app URL, e.g. https://brightfeed.vercel.app
_frontend_url = os.getenv("FRONTEND_URL", "")
_allowed_origins = [_frontend_url] if _frontend_url else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(articles.router, prefix="/api")
app.include_router(categories.router, prefix="/api")


# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"status": "ok", "message": "BrightFeed API is running 🌟"}


# ── Manual Fetch Trigger ──────────────────────────────────────────────────────
@app.post("/api/fetch-news", tags=["admin"])
async def trigger_fetch():
    """Manually trigger a news fetch from NewsAPI. Returns fetch statistics."""
    result = await fetch_and_store_news(settings.news_api_key)
    return result
