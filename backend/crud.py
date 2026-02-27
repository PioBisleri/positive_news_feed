from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Article, Category, Reaction
from schemas import ArticleCreate


# ── Categories ────────────────────────────────────────────────────────────────

async def get_categories(db: AsyncSession) -> List[Category]:
    result = await db.execute(select(Category).order_by(Category.name))
    return list(result.scalars().all())


# ── Articles ──────────────────────────────────────────────────────────────────

def _article_query():
    return (
        select(Article)
        .options(
            selectinload(Article.category),
            selectinload(Article.reactions),
        )
    )


async def get_articles(
    db: AsyncSession,
    category: Optional[str] = None,
    search: Optional[str] = None,
    featured: Optional[bool] = None,
) -> List[Article]:
    q = _article_query()

    if category:
        q = q.join(Article.category).where(Category.name.ilike(category))
    if search:
        q = q.where(
            or_(
                Article.title.ilike(f"%{search}%"),
                Article.summary.ilike(f"%{search}%"),
            )
        )
    if featured is not None:
        q = q.where(Article.is_featured == featured)

    q = q.order_by(Article.published_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_saved_articles(db: AsyncSession) -> List[Article]:
    q = _article_query().where(Article.is_saved == True).order_by(Article.published_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_article(db: AsyncSession, article_id: int) -> Optional[Article]:
    q = _article_query().where(Article.id == article_id)
    result = await db.execute(q)
    return result.scalars().first()


async def create_article(db: AsyncSession, article_data: ArticleCreate) -> Article:
    article = Article(**article_data.model_dump())
    db.add(article)
    await db.commit()
    await db.refresh(article)
    # Reload with relationships
    return await get_article(db, article.id)  # type: ignore[return-value]


async def toggle_save(db: AsyncSession, article_id: int) -> Optional[Article]:
    article = await get_article(db, article_id)
    if not article:
        return None
    article.is_saved = not article.is_saved
    await db.commit()
    await db.refresh(article)
    return await get_article(db, article_id)


async def add_reaction(
    db: AsyncSession, article_id: int, reaction_type: str
) -> Optional[Reaction]:
    result = await db.execute(
        select(Reaction).where(
            Reaction.article_id == article_id,
            Reaction.reaction_type == reaction_type,
        )
    )
    reaction = result.scalars().first()
    if not reaction:
        # Create a new reaction row
        reaction = Reaction(article_id=article_id, reaction_type=reaction_type, count=1)
        db.add(reaction)
    else:
        reaction.count += 1
    await db.commit()
    await db.refresh(reaction)
    return reaction
