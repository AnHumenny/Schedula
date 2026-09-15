from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.locations.buildings.models import Building


class BuildingRepository:
    """Repository for Building CRUD and query operations."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with an async database session."""
        self.session = session

    async def get_by_id(self, building_id: int) -> Optional[Building]:
        """Get a building by ID with rooms eager-loaded."""
        q = (
            select(Building)
            .where(Building.id == building_id)
            .options(selectinload(Building.rooms))
        )
        return (await self.session.execute(q)).scalar_one_or_none()


    async def get_by_name(self, name: str) -> Optional[Building]:
        """Get a building by unique name with rooms eager-loaded."""
        q = (
            select(Building)
            .where(Building.name == name)
            .options(selectinload(Building.rooms))
        )
        return (await self.session.execute(q)).scalar_one_or_none()


    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[Building]:
        """List buildings with optional active filter, pagination and name ordering."""
        q = select(Building)
        if only_active:
            q = q.where(Building.is_active.is_(True))
        q = q.order_by(Building.name).limit(limit).offset(offset)
        return list((await self.session.execute(q)).scalars().all())


    async def count(self, only_active: bool = False) -> int:
        """Count buildings, optionally only active ones."""
        q = select(func.count()).select_from(Building)
        if only_active:
            q = q.where(Building.is_active.is_(True))
        return (await self.session.execute(q)).scalar_one()


    async def create(self, building: Building) -> Building:
        """Persist a new building and return it with rooms refreshed."""
        self.session.add(building)
        await self.session.commit()
        await self.session.refresh(building, attribute_names=["rooms"])
        return building


    async def update(self, building: Building) -> Building:
        """Commit changes to an existing building and return it."""
        await self.session.commit()
        await self.session.refresh(building, attribute_names=["rooms"])
        return building


    async def delete(self, building: Building) -> None:
        """Delete the given building from the database."""
        await self.session.delete(building)
        await self.session.commit()