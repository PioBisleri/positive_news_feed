from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import articles, categories, reactions

app = FastAPI(
    title="BrightFeed API",
    description="Positive news feed — uplifting stories for a better day.",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(articles.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(reactions.router, prefix="/api")


# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"status": "ok", "message": "BrightFeed API is running 🌟"}
