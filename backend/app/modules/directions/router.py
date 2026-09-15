from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.deps import require_admin, get_current_user
from app.core.rate_limiter import RateLimits, limiter
from app.modules.directions.schemas import (
    DirectionCreate,
    DirectionUpdate,
    DirectionRead,
)
from app.modules.directions.service import DirectionService
from app.modules.directions.dependencies import get_direction_service
from app.modules.users.models import User

router = APIRouter(prefix="/directions", tags=["directions"])


@limiter.limit(RateLimits.READ)
@router.get("/", response_model=List[DirectionRead])
async def list_directions(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    only_active: bool = False,
    service: DirectionService = Depends(get_direction_service),
    _: User = Depends(get_current_user),
):
    """List directions with optional active filter and pagination."""
    return await service.list_directions(limit, offset, only_active)


@limiter.limit(RateLimits.READ)
@router.get("/{direction_id}", response_model=DirectionRead)
async def get_direction(
    request: Request,
    direction_id: int,
    service: DirectionService = Depends(get_direction_service),
    _: User = Depends(get_current_user),
):
    """Get a single direction by ID."""
    try:
        return await service.get_direction(direction_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.post("/", response_model=DirectionRead, status_code=201)
async def create_direction(
    request: Request,
    data: DirectionCreate,
    service: DirectionService = Depends(get_direction_service),
    _: User = Depends(require_admin),
):
    """Create a new direction (admin only)."""
    try:
        return await service.create_direction(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.patch("/{direction_id}", response_model=DirectionRead)
async def update_direction(
    request: Request,
    direction_id: int,
    data: DirectionUpdate,
    service: DirectionService = Depends(get_direction_service),
    _: User = Depends(require_admin),
):
    """Update an existing direction (admin only)."""
    try:
        return await service.update_direction(direction_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.READ)
@router.delete("/{direction_id}", status_code=204)
async def delete_direction(
    request: Request,
    direction_id: int,
    service: DirectionService = Depends(get_direction_service),
    _: User = Depends(require_admin),
):
    """Delete a direction by ID (admin only)."""
    try:
        await service.delete_direction(direction_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
