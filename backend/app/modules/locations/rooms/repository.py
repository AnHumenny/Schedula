from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.locations.rooms.models import Room


class RoomRepository:
    """Repository for managing room data persistence."""

    def __init__(self, session: AsyncSession):
        """Initialize the room repository."""
        self.session = session

    async def get_by_id(self, room_id: int) -> Optional[Room]:
        """Retrieve a room by its ID."""
        return await self.session.get(Room, room_id)


    async def get_by_building_and_number(
        self, building_id: int, number: str
    ) -> Optional[Room]:
        """Retrieve a room by its building ID and number."""
        q = select(Room).where(
            Room.building_id == building_id,
            Room.number == number,
        )
        return (await self.session.execute(q)).scalar_one_or_none()


    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
        building_id: int | None = None,
    ) -> List[Room]:
        """Retrieve a list of rooms with optional filters and pagination."""
        q = select(Room)
        if building_id is not None:
            q = q.where(Room.building_id == building_id)
        if only_active:
            q = q.where(Room.is_active.is_(True))
        q = (
            q.order_by(Room.building_id, Room.number)
            .limit(limit)
            .offset(offset)
        )
        return list((await self.session.execute(q)).scalars().all())


    async def list_by_building(
        self,
        building_id: int,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[Room]:
        """Retrieve a list of rooms for a specified building."""
        return await self.list(limit, offset, only_active, building_id)


    async def count(
        self,
        building_id: int | None = None,
        only_active: bool = False,
    ) -> int:
        """Count rooms matching the optional filters."""
        q = select(func.count()).select_from(Room)
        if building_id is not None:
            q = q.where(Room.building_id == building_id)
        if only_active:
            q = q.where(Room.is_active.is_(True))
        return (await self.session.execute(q)).scalar_one()


    async def create(self, room: Room) -> Room:
        """Create a new room record."""
        self.session.add(room)
        await self.session.commit()
        await self.session.refresh(room)
        return room


    async def update(self, room: Room) -> Room:
        """Update an existing room record."""
        await self.session.commit()
        await self.session.refresh(room)
        return room


    async def delete(self, room: Room) -> None:
        """Delete a room record."""
        await self.session.delete(room)
        await self.session.commit()