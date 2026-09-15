from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.locations.buildings.repository import BuildingRepository
from app.modules.locations.buildings.service import BuildingService


async def get_building_repository(
    session: AsyncSession = Depends(get_session),
) -> BuildingRepository:
    """Provide a BuildingRepository instance with the current database session."""
    return BuildingRepository(session)


async def get_building_service(
    repo: BuildingRepository = Depends(get_building_repository),
) -> BuildingService:
    """Provide a BuildingService instance with the current repository."""
    return BuildingService(repo)
