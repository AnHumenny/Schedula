from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.groups.models import Group


class GroupRepository:
    """Repository for Group CRUD and query operations."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with an async database session."""
        self.session = session

    async def get_by_id(self, group_id: int) -> Optional[Group]:
        """Get a group by its primary key."""
        return await self.session.get(Group, group_id)


    async def get_by_user_id(self, user_id: int) -> Optional[Group]:
        """Get a group by user_id (legacy; prefer users.group_id)."""
        q = select(Group).where(Group.user_id == user_id)
        return (await self.session.execute(q)).scalar_one_or_none()


    async def get_by_direction(
        self,
        direction_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Group]:
        """List groups belonging to a direction with pagination."""
        q = (
            select(Group)
            .where(Group.direction_id == direction_id)
            .order_by(Group.name)
            .limit(limit)
            .offset(offset)
        )
        return list((await self.session.execute(q)).scalars().all())


    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[Group]:
        """List groups with optional active filter, pagination and name ordering."""
        q = select(Group)
        if only_active:
            q = q.where(Group.is_active.is_(True))
        q = q.order_by(Group.name).limit(limit).offset(offset)
        return list((await self.session.execute(q)).scalars().all())


    async def count(self, only_active: bool = False) -> int:
        """Count groups, optionally only active ones."""
        q = select(func.count()).select_from(Group)
        if only_active:
            q = q.where(Group.is_active.is_(True))
        return (await self.session.execute(q)).scalar_one()


    async def create(self, group: Group) -> Group:
        """Persist a new group and return it."""
        self.session.add(group)
        await self.session.commit()
        await self.session.refresh(group)
        return group


    async def update(self, group: Group) -> Group:
        """Commit changes to an existing group and return it."""
        await self.session.commit()
        await self.session.refresh(group)
        return group


    async def delete(self, group: Group) -> None:
        """Delete the given group from the database."""
        await self.session.delete(group)
        await self.session.commit()