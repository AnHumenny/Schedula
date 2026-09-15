from typing import TYPE_CHECKING, List

from app.modules.groups.models import Group
from app.modules.groups.repository import GroupRepository
from app.modules.groups.schemas import (
    GroupCreate,
    GroupRead,
    GroupUpdate,
)

if TYPE_CHECKING:
    from app.modules.users.repository import UserRepository
    from app.modules.directions.repository import DirectionRepository


class GroupService:
    """Service layer for academic groups (User N:1 Group N:1 Direction)."""

    def __init__(
        self,
        repo: GroupRepository,
        user_repo: "UserRepository",
        direction_repo: "DirectionRepository",
    ):
        """Initialize service with group, user and direction repositories."""
        self.repo = repo
        self.user_repo = user_repo
        self.direction_repo = direction_repo

    async def _ensure_direction_exists(self, direction_id: int) -> None:
        """Raise ValueError if the direction does not exist."""
        direction = await self.direction_repo.get_by_id(direction_id)
        if not direction:
            raise ValueError(f"Direction {direction_id} not found")


    async def _get_group_or_raise(self, group_id: int) -> Group:
        """Get group by ID or raise ValueError if not found."""
        group = await self.repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")
        return group


    async def _get_user_or_raise(self, user_id: int):
        """Get user by ID or raise ValueError if not found."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        return user


    async def get_group(self, group_id: int) -> GroupRead:
        """Get a group by ID or raise ValueError if not found."""
        group = await self._get_group_or_raise(group_id)
        return GroupRead.model_validate(group)


    async def list_groups(
        self,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[GroupRead]:
        """List groups with optional active filter and pagination."""
        groups = await self.repo.list(limit, offset, only_active)
        return [GroupRead.model_validate(g) for g in groups]


    async def list_by_direction(
        self,
        direction_id: int,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = False,
    ) -> List[GroupRead]:
        """List groups of a direction or raise ValueError if direction not found."""
        await self._ensure_direction_exists(direction_id)
        groups = await self.repo.get_by_direction(
            direction_id, limit, offset
        )
        return [GroupRead.model_validate(g) for g in groups]


    async def get_group_by_user(self, user_id: int) -> GroupRead:
        """Get the group assigned to a user or raise ValueError if none."""
        user = await self._get_user_or_raise(user_id)
        if user.group_id is None:
            raise ValueError(f"User {user_id} is not assigned to any group")
        return await self.get_group(user.group_id)


    async def list_group_members(
        self,
        group_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> list:
        """List users belonging to the group (returns ORM User objects)."""
        await self._get_group_or_raise(group_id)
        return await self.user_repo.list_by_group(group_id, limit, offset)


    async def create_group(self, data: GroupCreate) -> GroupRead:
        """Create a group after verifying the direction exists."""
        await self._ensure_direction_exists(data.direction_id)

        group = Group(**data.model_dump())
        group = await self.repo.create(group)
        return GroupRead.model_validate(group)


    async def update_group(
        self,
        group_id: int,
        data: GroupUpdate,
    ) -> GroupRead:
        """Update a group or raise ValueError if not found / direction missing."""
        group = await self._get_group_or_raise(group_id)

        payload = data.model_dump(exclude_unset=True)

        if "direction_id" in payload and payload["direction_id"] != group.direction_id:
            await self._ensure_direction_exists(payload["direction_id"])

        for field, value in payload.items():
            setattr(group, field, value)

        group = await self.repo.update(group)
        return GroupRead.model_validate(group)


    async def delete_group(self, group_id: int) -> None:
        """Delete a group (users.group_id set to NULL, schedule items cascade)."""
        group = await self._get_group_or_raise(group_id)
        await self.repo.delete(group)


    async def assign_user(self, group_id: int, user_id: int) -> GroupRead:
        """Assign a user to a group (fails if already in another group)."""
        group = await self._get_group_or_raise(group_id)
        user = await self._get_user_or_raise(user_id)

        if user.group_id == group.id:
            return GroupRead.model_validate(group)

        if user.group_id is not None:
            raise ValueError(
                f"User {user_id} already belongs to group {user.group_id}; "
                f"detach first or use reassign"
            )

        user.group_id = group.id
        await self.user_repo.update(user)
        return GroupRead.model_validate(group)


    async def reassign_user(self, group_id: int, user_id: int) -> GroupRead:
        """Move a user to another group (explicit reassignment)."""
        group = await self._get_group_or_raise(group_id)
        user = await self._get_user_or_raise(user_id)

        user.group_id = group.id
        await self.user_repo.update(user)
        return GroupRead.model_validate(group)


    async def detach_user(self, user_id: int) -> None:
        """Remove a user from their group (set group_id to NULL)."""
        user = await self._get_user_or_raise(user_id)
        if user.group_id is None:
            return

        user.group_id = None
        await self.user_repo.update(user)
