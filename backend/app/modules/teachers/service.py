from typing import List

from app.modules.teachers.models import Teacher
from app.modules.teachers.repository import TeacherRepository
from app.modules.teachers.schemas import (
    TeacherCreate,
    TeacherRead,
    TeacherUpdate,
)


class TeacherService:
    """Service for managing teachers."""

    def __init__(self, repo: TeacherRepository):
        """Initialize the teacher service."""
        self.repo = repo

    @staticmethod
    def _to_read(teacher: Teacher) -> TeacherRead:
        """Convert a teacher model to a read DTO."""
        return TeacherRead(
            id=teacher.id,
            fullname=teacher.fullname,
            description=teacher.description,
            is_active=teacher.is_active,
            created_at=teacher.created_at,
            updated_at=teacher.updated_at,
            discipline_ids=[d.id for d in teacher.disciplines],
        )


    async def _resolve_disciplines(self, discipline_ids: list[int]) -> list:
        """Load and validate disciplines by their IDs."""
        if not discipline_ids:
            return []
        unique_ids = list({*discipline_ids})
        disciplines = await self.repo.get_disciplines_by_ids(unique_ids)
        found_ids = {d.id for d in disciplines}
        missing = set(unique_ids) - found_ids
        if missing:
            raise ValueError(f"Disciplines not found: {sorted(missing)}")
        return disciplines


    async def get_teacher(self, teacher_id: int) -> TeacherRead:
        """Retrieve a teacher by their ID."""
        teacher = await self.repo.get_by_id(teacher_id)
        if not teacher:
            raise ValueError("Teacher not found")
        return self._to_read(teacher)


    async def list_teachers(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[TeacherRead]:
        """Retrieve a list of teachers with pagination and filters."""
        teachers = await self.repo.list(limit, offset, only_active)
        return [self._to_read(t) for t in teachers]


    async def create_teacher(self, data: TeacherCreate) -> TeacherRead:
        """Create a new teacher."""
        existing = await self.repo.get_by_fullname(data.fullname)
        if existing:
            raise ValueError(
                f"Teacher with fullname '{data.fullname}' already exists"
            )

        disciplines = await self._resolve_disciplines(data.discipline_ids)

        teacher = Teacher(
            fullname=data.fullname,
            description=data.description,
        )
        teacher.disciplines = disciplines

        teacher = await self.repo.create(teacher)
        return self._to_read(teacher)

    async def update_teacher(
        self,
        teacher_id: int,
        data: TeacherUpdate,
    ) -> TeacherRead:
        """Update an existing teacher."""
        teacher = await self.repo.get_by_id(teacher_id)
        if not teacher:
            raise ValueError("Teacher not found")

        payload = data.model_dump(exclude_unset=True)

        if "fullname" in payload and payload["fullname"] != teacher.fullname:
            existing = await self.repo.get_by_fullname(payload["fullname"])
            if existing:
                raise ValueError(
                    f"Teacher with fullname '{payload['fullname']}' already exists"
                )

        for field in ("fullname", "description", "is_active"):
            if field in payload:
                setattr(teacher, field, payload[field])

        if "discipline_ids" in payload and payload["discipline_ids"] is not None:
            disciplines = await self._resolve_disciplines(
                payload["discipline_ids"]
            )
            teacher.disciplines = disciplines

        teacher = await self.repo.update(teacher)
        return self._to_read(teacher)


    async def delete_teacher(self, teacher_id: int) -> None:
        """Delete a teacher by their ID."""
        teacher = await self.repo.get_by_id(teacher_id)
        if not teacher:
            raise ValueError("Teacher not found")
        await self.repo.delete(teacher)


    async def list_by_discipline(
            self,
            discipline_id: int,
            limit: int = 50,
            offset: int = 0,
            only_active: bool = False,
    ) -> List[TeacherRead]:
        """Retrieve teachers associated with a specific discipline."""
        from app.modules.disciplines.repository import DisciplineRepository
        discipline_repo = DisciplineRepository(self.repo.session)
        discipline = await discipline_repo.get_by_id(discipline_id)
        if not discipline:
            raise ValueError(f"Discipline {discipline_id} not found")

        teachers = await self.repo.list_by_discipline(
            discipline_id, limit, offset, only_active
        )
        return [self._to_read(t) for t in teachers]
