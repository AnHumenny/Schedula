from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.teachers.repository import TeacherRepository
from app.modules.teachers.service import TeacherService


async def get_teacher_repository(
    session: AsyncSession = Depends(get_session),
) -> TeacherRepository:
    """Provide a TeacherRepository instance."""
    return TeacherRepository(session)


async def get_teacher_service(
    repo: TeacherRepository = Depends(get_teacher_repository),
) -> TeacherService:
    """Provide a TeacherService instance."""
    return TeacherService(repo)
