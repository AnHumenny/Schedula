from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.deps import require_admin, get_current_user
from app.core.rate_limiter import RateLimits, limiter
from app.modules.groups.schemas import GroupCreate, GroupUpdate, GroupRead
from app.modules.groups.service import GroupService
from app.modules.groups.dependencies import get_group_service
from app.modules.users.models import User

router = APIRouter(prefix="/groups", tags=["groups"])


@limiter.limit(RateLimits.READ)
@router.get("/", response_model=List[GroupRead])
async def list_groups(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    only_active: bool = False,
    service: GroupService = Depends(get_group_service),
    _: User = Depends(get_current_user),
):
    """List groups with optional active filter and pagination."""
    return await service.list_groups(limit, offset, only_active)


@limiter.limit(RateLimits.READ)
@router.get("/by-direction/{direction_id}", response_model=List[GroupRead])
async def list_groups_by_direction(
    request: Request,
    direction_id: int,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    service: GroupService = Depends(get_group_service),
    _: User = Depends(get_current_user),
):
    """List groups belonging to a specific direction."""
    return await service.list_by_direction(direction_id, limit, offset)


@limiter.limit(RateLimits.READ)
@router.get("/by-user/{user_id}", response_model=GroupRead)
async def get_group_by_user(
    request: Request,
    user_id: int,
    service: GroupService = Depends(get_group_service),
    _: User = Depends(get_current_user),
):
    """Get the group assigned to a specific user."""
    try:
        return await service.get_group_by_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.READ)
@router.get("/{group_id}", response_model=GroupRead)
async def get_group(
    request: Request,
    group_id: int,
    service: GroupService = Depends(get_group_service),
    _: User = Depends(get_current_user),
):
    """Get a single group by ID."""
    try:
        return await service.get_group(group_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.post("/", response_model=GroupRead, status_code=201)
async def create_group(
    request: Request,
    data: GroupCreate,
    service: GroupService = Depends(get_group_service),
    _: User = Depends(require_admin),
):
    """Create a new group (admin only)."""
    try:
        return await service.create_group(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.patch("/{group_id}", response_model=GroupRead)
async def update_group(
    request: Request,
    group_id: int,
    data: GroupUpdate,
    service: GroupService = Depends(get_group_service),
    _: User = Depends(require_admin),
):
    """Update an existing group (admin only)."""
    try:
        return await service.update_group(group_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.delete("/{group_id}", status_code=204)
async def delete_group(
    request: Request,
    group_id: int,
    service: GroupService = Depends(get_group_service),
    _: User = Depends(require_admin),
):
    """Delete a group by ID (admin only)."""
    try:
        await service.delete_group(group_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))