from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.deps import get_current_user, require_admin
from app.core.rate_limiter import RateLimits, limiter
from app.modules.locations.buildings.dependencies import get_building_service
from app.modules.locations.buildings.schemas import (
    BuildingCreate,
    BuildingRead,
    BuildingUpdate,
)
from app.modules.locations.buildings.service import BuildingService
from app.modules.users.models import User

router = APIRouter(prefix="/buildings", tags=["buildings"])


@limiter.limit(RateLimits.READ)
@router.get("/", response_model=List[BuildingRead])
async def list_buildings(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    only_active: bool = False,
    service: BuildingService = Depends(get_building_service),
    _: User = Depends(get_current_user),
):
    """List buildings with optional active filter and pagination."""
    return await service.list_buildings(limit, offset, only_active)


@limiter.limit(RateLimits.READ)
@router.get("/{building_id}", response_model=BuildingRead)
async def get_building(
    request: Request,
    building_id: int,
    service: BuildingService = Depends(get_building_service),
    _: User = Depends(get_current_user),
):
    """Get a single building by ID."""
    try:
        return await service.get_building(building_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.post("/", response_model=BuildingRead, status_code=201)
async def create_building(
    request: Request,
    data: BuildingCreate,
    service: BuildingService = Depends(get_building_service),
    _: User = Depends(require_admin),
):
    """Create a new building (admin only)."""
    try:
        return await service.create_building(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.patch("/{building_id}", response_model=BuildingRead)
async def update_building(
    request: Request,
    building_id: int,
    data: BuildingUpdate,
    service: BuildingService = Depends(get_building_service),
    _: User = Depends(require_admin),
):
    """Update an existing building (admin only)."""
    try:
        return await service.update_building(building_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.delete("/{building_id}", status_code=204)
async def delete_building(
    request: Request,
    building_id: int,
    service: BuildingService = Depends(get_building_service),
    _: User = Depends(require_admin),
):
    """Delete a building by ID (admin only; fails if rooms exist)."""
    try:
        await service.delete_building(building_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))