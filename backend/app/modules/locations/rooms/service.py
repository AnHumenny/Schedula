from typing import TYPE_CHECKING, List

from app.modules.locations.rooms.models import Room
from app.modules.locations.rooms.repository import RoomRepository
from app.modules.locations.rooms.schemas import (
    RoomCreate,
    RoomRead,
    RoomUpdate,
)

if TYPE_CHECKING:
    from app.modules.locations.buildings.repository import BuildingRepository


class RoomService:
    """Service for managing rooms."""

    def __init__(
        self,
        repo: RoomRepository,
        building_repo: "BuildingRepository",
    ):
        """Initialize the room service."""
        self.repo = repo
        self.building_repo = building_repo

    async def _ensure_building_exists(self, building_id: int) -> None:
        """Verify that the building exists by its ID."""
        building = await self.building_repo.get_by_id(building_id)
        if not building:
            raise ValueError(f"Building {building_id} not found")


    async def get_room(self, room_id: int) -> RoomRead:
        """Retrieve a room by its ID."""
        room = await self.repo.get_by_id(room_id)
        if not room:
            raise ValueError("Room not found")
        return RoomRead.model_validate(room)

    async def list_rooms(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
        building_id: int | None = None,
    ) -> List[RoomRead]:
        """Retrieve a list of rooms with filters and pagination."""
        rooms = await self.repo.list(limit, offset, only_active, building_id)
        return [RoomRead.model_validate(r) for r in rooms]

    async def list_by_building(
        self,
        building_id: int,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[RoomRead]:
        """Retrieve a list of rooms for a specified building."""
        await self._ensure_building_exists(building_id)
        rooms = await self.repo.list_by_building(
            building_id, limit, offset, only_active
        )
        return [RoomRead.model_validate(r) for r in rooms]


    async def create_room(self, data: RoomCreate) -> RoomRead:
        """Create a new room."""
        await self._ensure_building_exists(data.building_id)

        existing = await self.repo.get_by_building_and_number(
            data.building_id, data.number
        )
        if existing:
            raise ValueError(
                f"Room '{data.number}' already exists "
                f"in building {data.building_id}"
            )

        room = Room(**data.model_dump())
        room = await self.repo.create(room)
        return RoomRead.model_validate(room)

    async def update_room(
        self,
        room_id: int,
        data: RoomUpdate,
    ) -> RoomRead:
        """Update an existing room."""
        room = await self.repo.get_by_id(room_id)
        if not room:
            raise ValueError("Room not found")

        payload = data.model_dump(exclude_unset=True)

        new_building_id = payload.get("building_id", room.building_id)
        new_number = payload.get("number", room.number)

        if (
            "building_id" in payload and payload["building_id"] != room.building_id
        ) or ("number" in payload and payload["number"] != room.number):
            await self._ensure_building_exists(new_building_id)

            existing = await self.repo.get_by_building_and_number(
                new_building_id, new_number
            )
            if existing and existing.id != room.id:
                raise ValueError(
                    f"Room '{new_number}' already exists "
                    f"in building {new_building_id}"
                )

        for field, value in payload.items():
            setattr(room, field, value)

        room = await self.repo.update(room)
        return RoomRead.model_validate(room)


    async def delete_room(self, room_id: int) -> None:
        """Delete a room by its ID."""
        room = await self.repo.get_by_id(room_id)
        if not room:
            raise ValueError("Room not found")
        await self.repo.delete(room)