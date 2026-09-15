from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.directions.models import Direction


class DirectionRepository:
    """Repository for Direction CRUD and query operations."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with an async database session."""
        self.session = session


    async def get_by_id(self, direction_id: int) -> Optional[Direction]:
        """Get a direction by its primary key."""
        return await self.session.get(Direction, direction_id)


    async def get_by_name(self, name: str) -> Optional[Direction]:
        """Get a direction by its unique name."""
        q = select(Direction).where(Direction.name == name)
        return (await self.session.execute(q)).scalar_one_or_none()


    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[Direction]:
        """List directions with optional active filter, pagination and name ordering."""
        q = select(Direction)
        if only_active:
            q = q.where(Direction.is_active.is_(True))
        q = q.order_by(Direction.name).limit(limit).offset(offset)
        return list((await self.session.execute(q)).scalars().all())


    async def count(self, only_active: bool = False) -> int:
        """Count directions, optionally only active ones."""
        q = select(func.count()).select_from(Direction)
        if only_active:
            q = q.where(Direction.is_active.is_(True))
        return (await self.session.execute(q)).scalar_one()


    async def create(self, direction: Direction) -> Direction:
        """Persist a new direction and return it."""
        self.session.add(direction)
        await self.session.commit()
        await self.session.refresh(direction)
        return direction


    async def update(self, direction: Direction) -> Direction:
        """Commit changes to an existing direction and return it."""
        await self.session.commit()
        await self.session.refresh(direction)
        return direction


    async def delete(self, direction: Direction) -> None:
        """Delete the given direction from the database."""
        await self.session.delete(direction)
        await self.session.commit()
