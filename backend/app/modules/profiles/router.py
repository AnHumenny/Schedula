from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.deps import require_admin, get_current_user
from app.core.rate_limiter import RateLimits, limiter
from app.modules.profiles.dependencies import get_profile_service
from app.modules.profiles.schemas import (
    ProfileCreate,
    ProfileRead,
    ProfileUpdate,
)
from app.modules.profiles.service import ProfileService
from app.modules.users.models import User

router = APIRouter(prefix="/profiles", tags=["profiles"])


@limiter.limit(RateLimits.READ)
@router.get("/", response_model=List[ProfileRead])
async def list_profiles(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    only_active: bool = False,
    service: ProfileService = Depends(get_profile_service),
    _: User = Depends(get_current_user),
):
    """Retrieve a list of profiles with optional pagination and filters."""
    return await service.list_profiles(limit, offset, only_active)


@limiter.limit(RateLimits.READ)
@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile(
    request: Request,
    profile_id: int,
    service: ProfileService = Depends(get_profile_service),
    _: User = Depends(get_current_user),
):
    """Retrieve a specific profile by its unique identifier."""
    try:
        return await service.get_profile(profile_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.post("/", response_model=ProfileRead, status_code=201)
async def create_profile(
    request: Request,
    data: ProfileCreate,
    service: ProfileService = Depends(get_profile_service),
    _: User = Depends(require_admin),
):
    """Create a new profile (admin only)."""
    try:
        return await service.create_profile(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.patch("/{profile_id}", response_model=ProfileRead)
async def update_profile(
    request: Request,
    profile_id: int,
    data: ProfileUpdate,
    service: ProfileService = Depends(get_profile_service),
    _: User = Depends(require_admin),
):
    """Update an existing profile (admin only)."""
    try:
        return await service.update_profile(profile_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.delete("/{profile_id}", status_code=204)
async def delete_profile(
    request: Request,
    profile_id: int,
    service: ProfileService = Depends(get_profile_service),
    _: User = Depends(require_admin),
):
    """Delete a profile by its unique identifier (admin only)."""
    try:
        await service.delete_profile(profile_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
