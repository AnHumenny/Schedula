from datetime import datetime, timezone, timedelta
from typing import List

from sqlalchemy import select

from app.modules.schedule.repository import ScheduleRepository
from app.modules.schedule.schemas import (
    ScheduleItemCreate,
    ScheduleItemUpdate,
    ScheduleItemRead,
)
from app.modules.schedule.models import ScheduleItem


def _naive(dt: datetime) -> datetime:
    """Convert datetime to naive UTC."""
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


class ScheduleService:
    """Service for managing schedule items."""

    def __init__(self, repo: ScheduleRepository):
        """Initialize the schedule service."""
        self.repo = repo

    @staticmethod
    def _to_read(item: ScheduleItem) -> ScheduleItemRead:
        """Convert a schedule item model to a read DTO."""
        return ScheduleItemRead(
            id=item.id,
            group_ids=[g.id for g in item.groups],
            teacher_id=item.teacher_id,
            discipline_id=item.discipline_id,
            room_id=item.room_id,
            start_datetime=item.start_datetime,
            end_datetime=item.end_datetime,
            lesson_type=item.lesson_type,
            status=item.status,
            description=item.description,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )


    async def _resolve_groups(self, group_ids: list[int]):
        """Load groups by their IDs."""
        if not group_ids:
            return []
        from app.modules.groups.models import Group

        q = select(Group).where(Group.id.in_(set(group_ids)))
        groups = list((await self.repo.session.execute(q)).scalars().all())

        found = {g.id for g in groups}
        missing = set(group_ids) - found
        if missing:
            raise ValueError(f"Groups not found: {sorted(missing)}")

        return groups


    async def get_item(self, item_id: int) -> ScheduleItemRead:
        """Retrieve a schedule item by its ID."""
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise ValueError("Schedule item not found")
        return self._to_read(item)


    async def list_items(
            self,
            limit: int = 50,
            offset: int = 0,
    ) -> List[ScheduleItemRead]:
        """Retrieve a list of schedule items with pagination."""
        items = await self.repo.list(limit, offset)
        return [self._to_read(i) for i in items]


    async def get_group_schedule(
            self, group_id: int, limit: int = 50, offset: int = 0
    ) -> List[ScheduleItemRead]:
        """Retrieve the schedule for a specific group."""
        items = await self.repo.get_by_group(group_id, limit, offset)
        return [self._to_read(i) for i in items]


    async def get_teacher_schedule(
            self, teacher_id: int, limit: int = 50, offset: int = 0
    ) -> List[ScheduleItemRead]:
        """Retrieve the schedule for a specific teacher."""
        items = await self.repo.get_by_teacher(teacher_id, limit, offset)
        return [self._to_read(i) for i in items]


    async def create_item(self, data: ScheduleItemCreate) -> ScheduleItemRead:
        """Create a new schedule item."""
        start = _naive(data.start_datetime)
        end = _naive(data.end_datetime)

        await self._check_conflicts(data.room_id, data.teacher_id, start, end)

        item = ScheduleItem(
            teacher_id=data.teacher_id,
            discipline_id=data.discipline_id,
            room_id=data.room_id,
            start_datetime=start,
            end_datetime=end,
            lesson_type=data.lesson_type,
            status=data.status,
            description=data.description,
        )

        item.groups = await self._resolve_groups(data.group_ids)

        item = await self.repo.create(item)
        return self._to_read(item)


    async def update_item(
            self,
            item_id: int,
            data: ScheduleItemUpdate,
    ) -> ScheduleItemRead:
        """Update an existing schedule item."""
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise ValueError("Schedule item not found")

        payload = data.model_dump(exclude_unset=True)

        if "group_ids" in payload:
            group_ids = payload.pop("group_ids")
            item.groups = await self._resolve_groups(group_ids or [])

        for field in ("start_datetime", "end_datetime"):
            if field in payload and payload[field] is not None:
                payload[field] = _naive(payload[field])

        new_room = payload.get("room_id", item.room_id)
        new_teacher = payload.get("teacher_id", item.teacher_id)
        new_start = payload.get("start_datetime", item.start_datetime)
        new_end = payload.get("end_datetime", item.end_datetime)

        if any(
                f in payload
                for f in ("room_id", "teacher_id", "start_datetime", "end_datetime")
        ):
            await self._check_conflicts(
                new_room, new_teacher, new_start, new_end, exclude_id=item_id
            )

        for field, value in payload.items():
            setattr(item, field, value)

        item = await self.repo.update(item)
        return self._to_read(item)


    async def delete_item(self, item_id: int) -> None:
        """Delete a schedule item by its ID."""
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise ValueError("Schedule item not found")
        await self.repo.delete(item)

    async def _check_conflicts(
            self,
            room_id: int,
            teacher_id: int,
            start: datetime,
            end: datetime,
            exclude_id: int | None = None,
    ) -> None:
        """Check for room scheduling conflicts."""
        conflicts = await self.repo.get_by_room_and_period(room_id, start, end)
        for c in conflicts:
            if exclude_id and c.id == exclude_id:
                continue
            raise ValueError(
                f"Room conflict with schedule item {c.id} "
                f"({c.start_datetime}–{c.end_datetime})"
            )


    async def get_upcoming(
            self,
            days: int = 7,
            group_id: int | None = None,
            teacher_id: int | None = None,
            limit: int = 200,
    ) -> List[ScheduleItemRead]:
        """Retrieve upcoming schedule items for a specified period."""
        now = datetime.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=days)

        items = await self.repo.get_upcoming(
            start=start,
            end=end,
            group_id=group_id,
            teacher_id=teacher_id,
            limit=limit,
        )
        return [self._to_read(i) for i in items]
