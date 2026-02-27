from datetime import datetime, timezone
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey,
    Integer, String, Text, func
)
from sqlalchemy.orm import relationship
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    emoji = Column(String(10))
    color = Column(String(50))

    articles = relationship("Article", back_populates="category")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=False)
    content = Column(Text)
    image_url = Column(String(1000))
    source = Column(String(200))
    author = Column(String(200))
    published_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_featured = Column(Boolean, default=False)
    is_saved = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    category = relationship("Category", back_populates="articles")
    reactions = relationship(
        "Reaction", back_populates="article", cascade="all, delete-orphan"
    )


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(
        Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False
    )
    reaction_type = Column(String(50), nullable=False)
    count = Column(Integer, default=0)

    article = relationship("Article", back_populates="reactions")
