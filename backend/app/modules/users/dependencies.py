from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService
from app.modules.groups.dependencies import get_group_repository
from app.modules.groups.repository import GroupRepository
from app.modules.profiles.dependencies import get_profile_repository
from app.modules.profiles.repository import ProfileRepository


async def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    """Provide a UserRepository instance."""
    return UserRepository(session)


async def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
    group_repo: GroupRepository = Depends(get_group_repository),
    profile_repo: ProfileRepository = Depends(get_profile_repository),
) -> UserService:
    """Provide a UserService instance."""
    return UserService(repo, group_repo, profile_repo)
