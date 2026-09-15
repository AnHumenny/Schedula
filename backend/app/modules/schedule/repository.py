from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.schedule.models import ScheduleItem


from sqlalchemy.orm import selectinload
from sqlalchemy import select, desc


class ScheduleRepository:
    """Repository for managing schedule item data persistence."""

    def __init__(self, session: AsyncSession):
        """Initialize the schedule repository."""
        self.session = session

    async def get_by_id(self, item_id: int) -> ScheduleItem | None:
        """Retrieve a schedule item by its ID."""
        q = (
            select(ScheduleItem)
            .where(ScheduleItem.id == item_id)
            .options(selectinload(ScheduleItem.groups))
        )
        return (await self.session.execute(q)).scalar_one_or_none()


    async def list(self, limit: int = 50, offset: int = 0) -> List[ScheduleItem]:
        """Retrieve a list of schedule items with pagination."""
        q = (
            select(ScheduleItem)
            .options(selectinload(ScheduleItem.groups))
            .order_by(ScheduleItem.start_datetime)
            .limit(limit)
            .offset(offset)
        )
        return list((await self.session.execute(q)).scalars().all())


    async def get_by_group(
        self, group_id: int, limit: int = 50, offset: int = 0
    ) -> List[ScheduleItem]:
        """Retrieve schedule items for a specific group."""
        from app.modules.groups.models import Group

        q = (
            select(ScheduleItem)
            .join(ScheduleItem.groups)
            .where(Group.id == group_id)
            .options(selectinload(ScheduleItem.groups))
            .order_by(desc(ScheduleItem.start_datetime))
            .limit(limit)
            .offset(offset)
        )
        return list((await self.session.execute(q)).scalars().all())


    async def get_by_teacher(
        self, teacher_id: int, limit: int = 50, offset: int = 0
    ) -> List[ScheduleItem]:
        """Retrieve schedule items for a specific teacher."""
        q = (
            select(ScheduleItem)
            .where(ScheduleItem.teacher_id == teacher_id)
            .options(selectinload(ScheduleItem.groups))
            .order_by(desc(ScheduleItem.start_datetime))
            .limit(limit)
            .offset(offset)
        )
        return list((await self.session.execute(q)).scalars().all())


    async def get_by_room_and_period(
        self, room_id: int, start: datetime, end: datetime
    ) -> List[ScheduleItem]:
        """Retrieve schedule items for a room within a specified period."""
        q = (
            select(ScheduleItem)
            .where(
                ScheduleItem.room_id == room_id,
                ScheduleItem.start_datetime < end,
                ScheduleItem.end_datetime > start,
            )
        )
        return list((await self.session.execute(q)).scalars().all())


    async def create(self, item: ScheduleItem) -> ScheduleItem:
        """Create a new schedule item record."""
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item, attribute_names=["groups"])
        return item


    async def update(self, item: ScheduleItem) -> ScheduleItem:
        """Update an existing schedule item record."""
        await self.session.commit()
        await self.session.refresh(item, attribute_names=["groups"])
        return item


    async def delete(self, item: ScheduleItem) -> None:
        """Delete a schedule item record."""
        await self.session.delete(item)
        await self.session.commit()


    async def get_upcoming(
            self,
            start: datetime,
            end: datetime,
            group_id: int | None = None,
            teacher_id: int | None = None,
            limit: int = 200,
    ) -> List[ScheduleItem]:
        """Retrieve upcoming schedule items for a given period and filters."""
        q = (
            select(ScheduleItem)
            .where(
                ScheduleItem.start_datetime >= start,
                ScheduleItem.start_datetime <= end,
            )
            .options(selectinload(ScheduleItem.groups))
            .order_by(ScheduleItem.start_datetime)
            .limit(limit)
        )

        if group_id is not None:
            from app.modules.groups.models import Group
            q = q.join(ScheduleItem.groups).where(Group.id == group_id)

        if teacher_id is not None:
            q = q.where(ScheduleItem.teacher_id == teacher_id)

        return list((await self.session.execute(q)).scalars().all())
