from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# ── Category ──────────────────────────────────────────────────────────────────

class CategoryBase(BaseModel):
    name: str
    emoji: Optional[str] = None
    color: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ── Reaction ──────────────────────────────────────────────────────────────────

class ReactionResponse(BaseModel):
    id: int
    article_id: int
    reaction_type: str
    count: int

    model_config = ConfigDict(from_attributes=True)


class ReactionUpdate(BaseModel):
    reaction_type: str


# ── Article ───────────────────────────────────────────────────────────────────

class ArticleBase(BaseModel):
    title: str
    summary: str
    content: Optional[str] = None
    image_url: Optional[str] = None
    source: Optional[str] = None
    author: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: bool = False


class ArticleCreate(ArticleBase):
    pass


class ArticleResponse(ArticleBase):
    id: int
    published_at: Optional[datetime] = None
    is_saved: bool
    created_at: Optional[datetime] = None
    category: Optional[CategoryResponse] = None
    reactions: List[ReactionResponse] = []

    model_config = ConfigDict(from_attributes=True)
