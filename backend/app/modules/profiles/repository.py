from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.profiles.models import Profile
from app.modules.schedule.models import ScheduleItem


class ProfileRepository:
    """Repository for managing profile data persistence."""

    def __init__(self, session: AsyncSession):
        """Initialize the profile repository."""
        self.session = session

    async def get_by_id(self, profile_id: int) -> Optional[Profile]:
        """Retrieve a profile by its ID."""
        return await self.session.get(Profile, profile_id)


    async def get_by_name(self, name: str) -> Optional[Profile]:
        """Retrieve a profile by its name."""
        q = select(Profile).where(Profile.name == name)
        return (await self.session.execute(q)).scalar_one_or_none()


    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[Profile]:
        """Retrieve a list of profiles with optional filters and pagination."""
        q = select(Profile)
        if only_active:
            q = q.where(Profile.is_active.is_(True))
        q = q.order_by(Profile.name).limit(limit).offset(offset)
        return list((await self.session.execute(q)).scalars().all())


    async def list_by_schedule_item(
        self,
        schedule_item_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Profile]:
        """Retrieve a list of profiles for a specified schedule item."""
        q = (
            select(Profile)
            .join(Profile.schedule_items)
            .where(ScheduleItem.id == schedule_item_id)
            .order_by(Profile.name)
            .limit(limit)
            .offset(offset)
        )
        return list((await self.session.execute(q)).scalars().all())


    async def count(self, only_active: bool = False) -> int:
        """Count profiles matching the optional active filter."""
        q = select(func.count()).select_from(Profile)
        if only_active:
            q = q.where(Profile.is_active.is_(True))
        return (await self.session.execute(q)).scalar_one()


    async def create(self, profile: Profile) -> Profile:
        """Create a new profile record."""
        self.session.add(profile)
        await self.session.commit()
        await self.session.refresh(profile)
        return profile


    async def update(self, profile: Profile) -> Profile:
        """Update an existing profile record."""
        await self.session.commit()
        await self.session.refresh(profile)
        return profile


    async def delete(self, profile: Profile) -> None:
        """Delete a profile record."""
        await self.session.delete(profile)
        await self.session.commit()
