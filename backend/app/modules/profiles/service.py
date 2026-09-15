from typing import List

from app.modules.profiles.models import Profile
from app.modules.profiles.repository import ProfileRepository
from app.modules.schedule.repository import ScheduleRepository
from app.modules.profiles.schemas import (
    ProfileCreate,
    ProfileRead,
    ProfileUpdate,
)


class ProfileService:
    """Service for managing profiles."""

    def __init__(self, repo: ProfileRepository):
        """Initialize the profile service."""
        self.repo = repo

    async def get_profile(self, profile_id: int) -> ProfileRead:
        """Retrieve a profile by its ID."""
        profile = await self.repo.get_by_id(profile_id)
        if not profile:
            raise ValueError("Profile not found")
        return ProfileRead.model_validate(profile)


    async def list_profiles(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[ProfileRead]:
        """Retrieve a list of profiles with optional pagination and filters."""
        profiles = await self.repo.list(limit, offset, only_active)
        return [ProfileRead.model_validate(p) for p in profiles]


    async def list_by_schedule_item(
        self,
        schedule_item_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> List[ProfileRead]:
        """Retrieve a list of profiles for a specified schedule item."""
        schedule_repo = ScheduleRepository(self.repo.session)
        item = await schedule_repo.get_by_id(schedule_item_id)
        if not item:
            raise ValueError(f"ScheduleItem {schedule_item_id} not found")

        profiles = await self.repo.list_by_schedule_item(
            schedule_item_id, limit, offset
        )
        return [ProfileRead.model_validate(p) for p in profiles]


    async def create_profile(self, data: ProfileCreate) -> ProfileRead:
        """Create a new profile."""
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise ValueError(
                f"Profile with name '{data.name}' already exists"
            )

        profile = Profile(**data.model_dump())
        profile = await self.repo.create(profile)
        return ProfileRead.model_validate(profile)


    async def update_profile(
        self,
        profile_id: int,
        data: ProfileUpdate,
    ) -> ProfileRead:
        """Update an existing profile."""
        profile = await self.repo.get_by_id(profile_id)
        if not profile:
            raise ValueError("Profile not found")

        payload = data.model_dump(exclude_unset=True)

        new_name = payload.get("name")
        if new_name and new_name != profile.name:
            existing = await self.repo.get_by_name(new_name)
            if existing:
                raise ValueError(
                    f"Profile with name '{new_name}' already exists"
                )

        for field, value in payload.items():
            setattr(profile, field, value)

        profile = await self.repo.update(profile)
        return ProfileRead.model_validate(profile)


    async def delete_profile(self, profile_id: int) -> None:
        """Delete a profile by its ID."""
        profile = await self.repo.get_by_id(profile_id)
        if not profile:
            raise ValueError("Profile not found")
        await self.repo.delete(profile)