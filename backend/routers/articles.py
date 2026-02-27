from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from database import get_db
from schemas import ArticleCreate, ArticleResponse, ReactionUpdate
import crud

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/saved", response_model=List[ArticleResponse])
async def list_saved_articles(db: AsyncSession = Depends(get_db)):
    return await crud.get_saved_articles(db)


@router.get("", response_model=List[ArticleResponse])
async def list_articles(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_articles(db, category=category, search=search, featured=featured)


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: AsyncSession = Depends(get_db)):
    article = await crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("", response_model=ArticleResponse, status_code=201)
async def create_article(article: ArticleCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_article(db, article)


@router.patch("/{article_id}/save", response_model=ArticleResponse)
async def toggle_save(article_id: int, db: AsyncSession = Depends(get_db)):
    article = await crud.toggle_save(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/{article_id}/react")
async def add_reaction(
    article_id: int,
    reaction: ReactionUpdate,
    db: AsyncSession = Depends(get_db),
):
    article = await crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    updated_reaction = await crud.add_reaction(db, article_id, reaction.reaction_type)
    return {
        "article_id": article_id,
        "reaction_type": reaction.reaction_type,
        "count": updated_reaction.count,
    }
