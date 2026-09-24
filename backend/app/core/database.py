from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy declarative models.

    Inherits from SQLAlchemy 2.0 DeclarativeBase to provide common functionality
    for all database models. All models should inherit from this class.
   """
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides a database session.

    Creates a new async database session for each request, commits on success
    and rolls back on exception, then closes the session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
