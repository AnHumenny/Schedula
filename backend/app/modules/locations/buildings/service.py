from typing import List

from app.modules.locations.buildings.models import Building
from app.modules.locations.buildings.repository import BuildingRepository
from app.modules.locations.buildings.schemas import (
    BuildingCreate,
    BuildingRead,
    BuildingUpdate,
)


class BuildingService:
    """Service layer for building business logic."""

    def __init__(self, repo: BuildingRepository):
        """Initialize service with a building repository."""
        self.repo = repo

    async def get_building(self, building_id: int) -> BuildingRead:
        """Get a building by ID or raise ValueError if not found."""
        building = await self.repo.get_by_id(building_id)
        if not building:
            raise ValueError("Building not found")
        return BuildingRead.model_validate(building)

    async def list_buildings(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[BuildingRead]:
        """List buildings with optional active filter and pagination."""
        buildings = await self.repo.list(limit, offset, only_active)
        return [BuildingRead.model_validate(b) for b in buildings]

    async def create_building(self, data: BuildingCreate) -> BuildingRead:
        """Create a new building or raise ValueError if name already exists."""
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise ValueError(
                f"Building with name '{data.name}' already exists"
            )

        building = Building(**data.model_dump())
        building = await self.repo.create(building)
        return BuildingRead.model_validate(building)

    async def update_building(
        self,
        building_id: int,
        data: BuildingUpdate,
    ) -> BuildingRead:
        """Update a building or raise ValueError if not found or name conflict."""
        building = await self.repo.get_by_id(building_id)
        if not building:
            raise ValueError("Building not found")

        payload = data.model_dump(exclude_unset=True)

        new_name = payload.get("name")
        if new_name and new_name != building.name:
            existing = await self.repo.get_by_name(new_name)
            if existing:
                raise ValueError(
                    f"Building with name '{new_name}' already exists"
                )

        for field, value in payload.items():
            setattr(building, field, value)

        building = await self.repo.update(building)
        return BuildingRead.model_validate(building)

    async def delete_building(self, building_id: int) -> None:
        """Delete a building or raise ValueError if not found or still has rooms."""
        building = await self.repo.get_by_id(building_id)
        if not building:
            raise ValueError("Building not found")

        if building.rooms:
            raise ValueError(
                f"Cannot delete building {building_id}: "
                f"it still has {len(building.rooms)} room(s)"
            )

        await self.repo.delete(building)
