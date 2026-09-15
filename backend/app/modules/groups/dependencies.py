from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.modules.groups.repository import GroupRepository
from app.modules.groups.service import GroupService
from app.modules.users.repository import UserRepository
from app.modules.directions.repository import DirectionRepository


async def get_group_repository(
    session: AsyncSession = Depends(get_session),
) -> GroupRepository:
    """Provide a GroupRepository instance with the current database session."""
    return GroupRepository(session)


async def get_group_service(
    repo: GroupRepository = Depends(get_group_repository),
    session: AsyncSession = Depends(get_session),
) -> GroupService:
    """Provide a GroupService instance with group, user and direction repositories."""
    user_repo = UserRepository(session)
    direction_repo = DirectionRepository(session)
    return GroupService(repo, user_repo, direction_repo)
