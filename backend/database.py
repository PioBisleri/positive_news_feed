import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

_raw_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/positivenews")

# Safely convert to asyncpg URL (avoid double-converting if already set)
if _raw_url.startswith("postgresql+asyncpg://"):
    ASYNC_DATABASE_URL = _raw_url
elif _raw_url.startswith("postgresql://"):
    ASYNC_DATABASE_URL = _raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    ASYNC_DATABASE_URL = _raw_url

# asyncpg does NOT support any query params in the URL (e.g. ?sslmode=require&channel_binding=require).
# Strip the entire query string and pass ssl via connect_args instead.
_has_ssl = "sslmode=require" in ASYNC_DATABASE_URL or "ssl" in ASYNC_DATABASE_URL
if "?" in ASYNC_DATABASE_URL:
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.split("?")[0]

_connect_args = {"ssl": "require"} if _has_ssl else {}

engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, connect_args=_connect_args)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
