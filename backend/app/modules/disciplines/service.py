from typing import List

from app.modules.disciplines.models import Discipline
from app.modules.teachers.repository import TeacherRepository
from app.modules.disciplines.repository import DisciplineRepository
from app.modules.disciplines.schemas import (
    DisciplineCreate,
    DisciplineRead,
    DisciplineUpdate,
)


class DisciplineService:
    """Service layer for discipline business logic."""

    def __init__(self, repo: DisciplineRepository):
        """Initialize service with a discipline repository."""
        self.repo = repo


    async def get_discipline(self, discipline_id: int) -> DisciplineRead:
        """Get a discipline by ID or raise ValueError if not found."""
        discipline = await self.repo.get_by_id(discipline_id)
        if not discipline:
            raise ValueError("Discipline not found")
        return DisciplineRead.model_validate(discipline)


    async def list_disciplines(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[DisciplineRead]:
        """List disciplines with optional active filter and pagination."""
        disciplines = await self.repo.list(limit, offset, only_active)
        return [DisciplineRead.model_validate(d) for d in disciplines]


    async def list_by_teacher(
        self,
        teacher_id: int,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[DisciplineRead]:
        """List disciplines for a teacher or raise ValueError if teacher not found."""
        teacher_repo = TeacherRepository(self.repo.session)
        teacher = await teacher_repo.get_by_id(teacher_id)
        if not teacher:
            raise ValueError(f"Teacher {teacher_id} not found")

        disciplines = await self.repo.list_by_teacher(
            teacher_id, limit, offset, only_active
        )
        return [DisciplineRead.model_validate(d) for d in disciplines]


    async def create_discipline(
        self, data: DisciplineCreate
    ) -> DisciplineRead:
        """Create a new discipline or raise ValueError if name already exists."""
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise ValueError(
                f"Discipline with name '{data.name}' already exists"
            )

        discipline = Discipline(**data.model_dump())
        discipline = await self.repo.create(discipline)
        return DisciplineRead.model_validate(discipline)


    async def update_discipline(
        self,
        discipline_id: int,
        data: DisciplineUpdate,
    ) -> DisciplineRead:
        """Update a discipline or raise ValueError if not found or name conflict."""
        discipline = await self.repo.get_by_id(discipline_id)
        if not discipline:
            raise ValueError("Discipline not found")

        payload = data.model_dump(exclude_unset=True)

        new_name = payload.get("name")
        if new_name and new_name != discipline.name:
            existing = await self.repo.get_by_name(new_name)
            if existing:
                raise ValueError(
                    f"Discipline with name '{new_name}' already exists"
                )

        for field, value in payload.items():
            setattr(discipline, field, value)

        discipline = await self.repo.update(discipline)
        return DisciplineRead.model_validate(discipline)


    async def delete_discipline(self, discipline_id: int) -> None:
        """Delete a discipline by ID or raise ValueError if not found."""
        discipline = await self.repo.get_by_id(discipline_id)
        if not discipline:
            raise ValueError("Discipline not found")
        await self.repo.delete(discipline)