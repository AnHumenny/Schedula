from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.modules.schedule.repository import ScheduleRepository
from app.modules.schedule.schedule_operations_repository import ScheduleOperationsRepository
from app.modules.schedule.service import ScheduleService


async def get_schedule_repository(
    session: AsyncSession = Depends(get_session),
) -> ScheduleRepository:
    """Dependency provider for the ScheduleRepository."""
    return ScheduleRepository(session)


async def get_schedule_service(
    repo: ScheduleRepository = Depends(get_schedule_repository),
) -> ScheduleService:
    """Dependency provider for the ScheduleService."""
    return ScheduleService(repo)


async def get_schedule_operation_repository(
    session: AsyncSession = Depends(get_session),
) -> ScheduleOperationsRepository:
    """Dependency provider for ScheduleOperationsRepository."""
    return ScheduleOperationsRepository(session)
