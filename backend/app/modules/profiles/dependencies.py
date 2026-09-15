from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.profiles.repository import ProfileRepository
from app.modules.profiles.service import ProfileService


async def get_profile_repository(
    session: AsyncSession = Depends(get_session),
) -> ProfileRepository:
    """Provide a ProfileRepository instance."""
    return ProfileRepository(session)


async def get_profile_service(
    repo: ProfileRepository = Depends(get_profile_repository),
) -> ProfileService:
    """Provide a ProfileService instance."""
    return ProfileService(repo)
