from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.locations.rooms.repository import RoomRepository
from app.modules.locations.rooms.service import RoomService
from app.modules.locations.buildings.dependencies import get_building_repository
from app.modules.locations.buildings.repository import BuildingRepository


async def get_room_repository(
    session: AsyncSession = Depends(get_session),
) -> RoomRepository:
    """Provide a RoomRepository instance."""
    return RoomRepository(session)


async def get_room_service(
    repo: RoomRepository = Depends(get_room_repository),
    building_repo: BuildingRepository = Depends(get_building_repository),
) -> RoomService:
    """Provide a RoomService instance."""
    return RoomService(repo, building_repo)
