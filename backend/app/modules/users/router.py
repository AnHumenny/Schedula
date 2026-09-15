from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.deps import require_admin
from app.core.rate_limiter import RateLimits, limiter
from app.modules.users.models import User
from app.modules.users.schemas import UserRead, UserCreate, UserUpdate
from app.modules.users.service import UserService
from app.modules.users.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])


@limiter.limit(RateLimits.READ)
@router.get("/", response_model=List[UserRead])
async def list_users(
    request: Request,
    limit: int = 50,
    offset: int = 0,
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_admin),
):
    """Retrieve a list of users with pagination (admin only)."""
    return await service.list_users(limit, offset)


@limiter.limit(RateLimits.READ)
@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    request: Request,
    user_id: int,
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_admin),
):
    """Retrieve a specific user by their ID (admin only)."""
    try:
        return await service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.READ)
@router.post("/", response_model=UserRead, status_code=201)
async def create_user(
    request: Request,
    data: UserCreate,
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_admin),
):
    """Create a new user account (admin only)."""
    return await service.create_user(data)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    request: Request,
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_admin),
):
    """Update an existing user account (admin only)."""
    try:
        return await service.update_user(user_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_admin),
):
    """Delete a user account by its ID (admin only)."""
    try:
        await service.delete_user(user_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
