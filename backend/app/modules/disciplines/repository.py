from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.disciplines.models import Discipline
from app.modules.teachers.models import Teacher


class DisciplineRepository:
    """Repository for Discipline CRUD and query operations."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with an async database session."""
        self.session = session


    async def get_by_id(self, discipline_id: int) -> Optional[Discipline]:
        """Get a discipline by its primary key."""
        return await self.session.get(Discipline, discipline_id)


    async def get_by_name(self, name: str) -> Optional[Discipline]:
        """Get a discipline by its unique name."""
        q = select(Discipline).where(Discipline.name == name)
        return (await self.session.execute(q)).scalar_one_or_none()


    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[Discipline]:
        """List disciplines with optional active filter, pagination and name ordering."""
        q = select(Discipline)
        if only_active:
            q = q.where(Discipline.is_active.is_(True))
        q = q.order_by(Discipline.name).limit(limit).offset(offset)
        return list((await self.session.execute(q)).scalars().all())


    async def list_by_teacher(
        self,
        teacher_id: int,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[Discipline]:
        """List disciplines associated with a specific teacher."""
        q = (
            select(Discipline)
            .join(Discipline.teachers)
            .where(Teacher.id == teacher_id)
        )
        if only_active:
            q = q.where(Discipline.is_active.is_(True))
        q = q.order_by(Discipline.name).limit(limit).offset(offset)
        return list((await self.session.execute(q)).scalars().all())


    async def count(self, only_active: bool = False) -> int:
        """Count disciplines, optionally only active ones."""
        q = select(func.count()).select_from(Discipline)
        if only_active:
            q = q.where(Discipline.is_active.is_(True))
        return (await self.session.execute(q)).scalar_one()


    async def create(self, discipline: Discipline) -> Discipline:
        """Persist a new discipline and return it."""
        self.session.add(discipline)
        await self.session.commit()
        await self.session.refresh(discipline)
        return discipline


    async def update(self, discipline: Discipline) -> Discipline:
        """Commit changes to an existing discipline and return it."""
        await self.session.commit()
        await self.session.refresh(discipline)
        return discipline


    async def delete(self, discipline: Discipline) -> None:
        """Delete the given discipline from the database."""
        await self.session.delete(discipline)
        await self.session.commit()