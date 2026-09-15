from typing import List
from app.modules.directions.repository import DirectionRepository
from app.modules.directions.schemas import (
    DirectionCreate,
    DirectionUpdate,
    DirectionRead,
)
from app.modules.directions.models import Direction


class DirectionService:
    """Service layer for direction business logic."""

    def __init__(self, repo: DirectionRepository):
        """Initialize service with a direction repository."""
        self.repo = repo

    async def get_direction(self, direction_id: int) -> DirectionRead:
        """Get a direction by ID or raise ValueError if not found."""
        direction = await self.repo.get_by_id(direction_id)
        if not direction:
            raise ValueError("Direction not found")
        return DirectionRead.model_validate(direction)

    async def list_directions(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[DirectionRead]:
        """List directions with optional active filter and pagination."""
        directions = await self.repo.list(limit, offset, only_active)
        return [DirectionRead.model_validate(d) for d in directions]

    async def create_direction(self, data: DirectionCreate) -> DirectionRead:
        """Create a new direction or raise ValueError if name already exists."""
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise ValueError(f"Direction with name '{data.name}' already exists")

        direction = Direction(**data.model_dump())
        direction = await self.repo.create(direction)
        return DirectionRead.model_validate(direction)

    async def update_direction(
        self,
        direction_id: int,
        data: DirectionUpdate,
    ) -> DirectionRead:
        """Update a direction or raise ValueError if not found or name conflict."""
        direction = await self.repo.get_by_id(direction_id)
        if not direction:
            raise ValueError("Direction not found")

        payload = data.model_dump(exclude_unset=True)

        new_name = payload.get("name")
        if new_name and new_name != direction.name:
            existing = await self.repo.get_by_name(new_name)
            if existing:
                raise ValueError(
                    f"Direction with name '{new_name}' already exists"
                )

        for field, value in payload.items():
            setattr(direction, field, value)

        direction = await self.repo.update(direction)
        return DirectionRead.model_validate(direction)

    async def delete_direction(self, direction_id: int) -> None:
        """Delete a direction by ID or raise ValueError if not found."""
        direction = await self.repo.get_by_id(direction_id)
        if not direction:
            raise ValueError("Direction not found")
        await self.repo.delete(direction)