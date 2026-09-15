from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.deps import get_current_user, require_admin
from app.core.rate_limiter import limiter, RateLimits
from app.modules.schedule.schemas import (
    ScheduleItemCreate, ScheduleItemUpdate, ScheduleItemRead
)
from app.modules.schedule.service import ScheduleService
from app.modules.schedule.dependencies import get_schedule_service
from app.modules.users.models import User

router = APIRouter(prefix="/schedule", tags=["schedule"])


@limiter.limit(RateLimits.READ)
@router.get("/upcoming", response_model=List[ScheduleItemRead])
async def upcoming_schedule(
    request: Request,
    days: int = Query(7, ge=1, le=30),
    group_id: int | None = Query(None),
    teacher_id: int | None = Query(None),
    limit: int = Query(200, ge=1, le=500),
    service: ScheduleService = Depends(get_schedule_service),
    _: User = Depends(get_current_user),
):
    """Retrieve upcoming schedule items with optional filters."""
    return await service.get_upcoming(
        days=days,
        group_id=group_id,
        teacher_id=teacher_id,
        limit=limit,
    )


@limiter.limit(RateLimits.READ)
@router.get("/group/{group_id}", response_model=List[ScheduleItemRead])
async def get_group_schedule(
    request: Request,
    group_id: int,
    limit: int = Query(50, le=200),
    offset: int = 0,
    service: ScheduleService = Depends(get_schedule_service),
    _: User = Depends(get_current_user),
):
    """Retrieve schedule items for a specific group."""
    return await service.get_group_schedule(group_id, limit, offset)


@limiter.limit(RateLimits.READ)
@router.get("/teacher/{teacher_id}", response_model=List[ScheduleItemRead])
async def get_teacher_schedule(
    request: Request,
    teacher_id: int,
    limit: int = Query(50, le=200),
    offset: int = 0,
    service: ScheduleService = Depends(get_schedule_service),
    _: User = Depends(get_current_user),
):
    """Retrieve schedule items for a specific teacher."""
    return await service.get_teacher_schedule(teacher_id, limit, offset)


@limiter.limit(RateLimits.READ)
@router.get("/", response_model=List[ScheduleItemRead])
async def list_schedule(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    service: ScheduleService = Depends(get_schedule_service),
    _: User = Depends(get_current_user),
):
    """Retrieve a list of all schedule items with pagination."""
    return await service.list_items(limit, offset)


@limiter.limit(RateLimits.READ)
@router.get("/{item_id}", response_model=ScheduleItemRead)
async def get_item(
    request: Request,
    item_id: int,
    service: ScheduleService = Depends(get_schedule_service),
    _: User = Depends(get_current_user),
):
    """Retrieve a specific schedule item by its ID."""
    try:
        return await service.get_item(item_id)
    except ValueError as e:
        raise HTTPException(404, str(e))


@limiter.limit(RateLimits.WRITE)
@router.post("/", response_model=ScheduleItemRead, status_code=201)
async def create_item(
    request: Request,
    data: ScheduleItemCreate,
    service: ScheduleService = Depends(get_schedule_service),
    _: User = Depends(require_admin),
):
    """Create a new schedule item (admin only)."""
    try:
        return await service.create_item(data)
    except ValueError as e:
        raise HTTPException(409, str(e))


@limiter.limit(RateLimits.WRITE)
@router.patch("/{item_id}", response_model=ScheduleItemRead)
async def update_item(
    request: Request,
    item_id: int,
    data: ScheduleItemUpdate,
    service: ScheduleService = Depends(get_schedule_service),
    _: User = Depends(require_admin),
):
    """Update an existing schedule item (admin only)."""
    try:
        return await service.update_item(item_id, data)
    except ValueError as e:
        raise HTTPException(404, str(e))


@limiter.limit(RateLimits.WRITE)
@router.delete("/{item_id}", status_code=204)
async def delete_item(
    request: Request,
    item_id: int,
    service: ScheduleService = Depends(get_schedule_service),
    _: User = Depends(require_admin),
):
    """Delete a schedule item by its ID (admin only)."""
    try:
        await service.delete_item(item_id)
    except ValueError as e:
        raise HTTPException(404, str(e))
