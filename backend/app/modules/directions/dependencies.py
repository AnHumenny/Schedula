from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.modules.directions.repository import DirectionRepository
from app.modules.directions.service import DirectionService


async def get_direction_repository(
    session: AsyncSession = Depends(get_session),
) -> DirectionRepository:
    """Provide a DirectionRepository instance with the current database session."""
    return DirectionRepository(session)


async def get_direction_service(
    repo: DirectionRepository = Depends(get_direction_repository),
) -> DirectionService:
    """Provide a DirectionService instance with the current repository."""
    return DirectionService(repo)
