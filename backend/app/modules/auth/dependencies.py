from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.auth.service import AuthService
from app.modules.users.repository import UserRepository


async def get_auth_service(
    session: AsyncSession = Depends(get_session),
) -> AuthService:
    """Provide an AuthService instance with the current database session."""
    return AuthService(UserRepository(session))