from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.deps import require_admin, get_current_user
from app.core.rate_limiter import RateLimits, limiter
from app.modules.locations.rooms.dependencies import get_room_service
from app.modules.locations.rooms.schemas import (
    RoomCreate,
    RoomRead,
    RoomUpdate,
)
from app.modules.locations.rooms.service import RoomService
from app.modules.users.models import User

router = APIRouter(prefix="/rooms", tags=["rooms"])


@limiter.limit(RateLimits.READ)
@router.get("/", response_model=List[RoomRead])
async def list_rooms(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    only_active: bool = False,
    building_id: int | None = Query(None, description="Filter by building ID"),
    service: RoomService = Depends(get_room_service),
    _: User = Depends(get_current_user),
):
    """Retrieve a list of rooms with optional filtering and pagination."""
    return await service.list_rooms(limit, offset, only_active, building_id)


@limiter.limit(RateLimits.READ)
@router.get("/by-building/{building_id}", response_model=List[RoomRead])
async def list_rooms_by_building(
    request: Request,
    building_id: int,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    only_active: bool = False,
    service: RoomService = Depends(get_room_service),
    _: User = Depends(get_current_user),
):
    """Retrieve a list of rooms belonging to a specific building."""
    try:
        return await service.list_by_building(building_id, limit, offset, only_active)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.READ)
@router.get("/{room_id}", response_model=RoomRead)
async def get_room(
    request: Request,
    room_id: int,
    service: RoomService = Depends(get_room_service),
    _: User = Depends(get_current_user),
):
    """Retrieve a specific room by its unique identifier."""
    try:
        return await service.get_room(room_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.post("/", response_model=RoomRead, status_code=201)
async def create_room(
    request: Request,
    data: RoomCreate,
    service: RoomService = Depends(get_room_service),
    _: User = Depends(require_admin),
):
    """Create a new room (admin only)."""
    try:
        return await service.create_room(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.patch("/{room_id}", response_model=RoomRead)
async def update_room(
    request: Request,
    room_id: int,
    data: RoomUpdate,
    service: RoomService = Depends(get_room_service),
    _: User = Depends(require_admin),
):
    """Update an existing room (admin only)."""
    try:
        return await service.update_room(room_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.delete("/{room_id}", status_code=204)
async def delete_room(
    request: Request,
    room_id: int,
    service: RoomService = Depends(get_room_service),
    _: User = Depends(require_admin),
):
    """Delete a room by its unique identifier (admin only)."""
    try:
        await service.delete_room(room_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
