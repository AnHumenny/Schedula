from typing import List, Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.teachers.models import Teacher
from app.modules.disciplines.models import Discipline


class TeacherRepository:
    """Repository for managing teacher data persistence."""

    def __init__(self, session: AsyncSession):
        """Initialize the teacher repository."""
        self.session = session


    async def get_by_id(self, teacher_id: int) -> Optional[Teacher]:
        """Retrieve a teacher by their ID."""
        return await self.session.get(Teacher, teacher_id)


    async def get_by_fullname(self, fullname: str) -> Optional[Teacher]:
        """Retrieve a teacher by their full name."""
        q = select(Teacher).where(Teacher.fullname == fullname)
        return (await self.session.execute(q)).scalar_one_or_none()


    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[Teacher]:
        """Retrieve a list of teachers with optional filters and pagination."""
        q = select(Teacher)
        if only_active:
            q = q.where(Teacher.is_active.is_(True))
        q = q.order_by(Teacher.fullname).limit(limit).offset(offset)
        return list((await self.session.execute(q)).scalars().all())


    async def count(self, only_active: bool = False) -> int:
        """Count teachers matching the optional active filter."""
        q = select(func.count()).select_from(Teacher)
        if only_active:
            q = q.where(Teacher.is_active.is_(True))
        return (await self.session.execute(q)).scalar_one()


    async def get_disciplines_by_ids(
        self, discipline_ids: Sequence[int]
    ) -> list:
        """Retrieve disciplines by their IDs."""
        from app.modules.disciplines.models import Discipline
        if not discipline_ids:
            return []
        q = select(Discipline).where(Discipline.id.in_(list(discipline_ids)))
        return list((await self.session.execute(q)).scalars().all())


    async def create(self, teacher: Teacher) -> Teacher:
        """Create a new teacher record."""
        self.session.add(teacher)
        await self.session.commit()
        await self.session.refresh(teacher)
        return teacher

    async def update(self, teacher: Teacher) -> Teacher:
        """Update an existing teacher record."""
        await self.session.commit()
        await self.session.refresh(teacher)
        return teacher


    async def delete(self, teacher: Teacher) -> None:
        """Delete a teacher record."""
        await self.session.delete(teacher)
        await self.session.commit()


    async def list_by_discipline(
            self,
            discipline_id: int,
            limit: int = 50,
            offset: int = 0,
            only_active: bool = False,
    ) -> List[Teacher]:
        """Retrieve teachers associated with a specific discipline."""

        q = (
            select(Teacher)
            .join(Teacher.disciplines)
            .where(Discipline.id == discipline_id)
        )
        if only_active:
            q = q.where(Teacher.is_active.is_(True))
        q = q.order_by(Teacher.fullname).limit(limit).offset(offset)
        return list((await self.session.execute(q)).scalars().all())
