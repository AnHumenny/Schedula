from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.disciplines.repository import DisciplineRepository
from app.modules.disciplines.service import DisciplineService


async def get_discipline_repository(
    session: AsyncSession = Depends(get_session),
) -> DisciplineRepository:
    """Provide a DisciplineRepository instance with the current database session."""
    return DisciplineRepository(session)


async def get_discipline_service(
    repo: DisciplineRepository = Depends(get_discipline_repository),
) -> DisciplineService:
    """Provide a DisciplineService instance with the current repository."""
    return DisciplineService(repo)