from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.deps import get_current_user, require_admin
from app.core.rate_limiter import limiter, RateLimits
from app.modules.schedule.schedule_operations_repository import ScheduleOperationsRepository
from app.modules.schedule.schemas import (
    ScheduleItemCreate, ScheduleItemUpdate, ScheduleItemRead, ScheduleCopyByGroupRequest,
    ScheduleCopyByDirectionRequest, ScheduleDeleteByDirectionRequest, ScheduleDeleteByGroupRequest
)
from app.modules.schedule.service import ScheduleService
from app.modules.schedule.dependencies import get_schedule_service, get_schedule_operation_repository
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
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0),
    service: ScheduleService = Depends(get_schedule_service),
    _: User = Depends(get_current_user),
):
    """Retrieve a list of all schedule items with pagination."""
    return await service.list_items(limit, offset)


@limiter.limit(RateLimits.READ)
@router.get("/range", response_model=List[ScheduleItemRead])
async def get_schedule_range(
    request: Request,
    start: datetime = Query(..., description="ISO 8601 with timezone"),
    end: datetime = Query(..., description="ISO 8601 with timezone"),
    service: ScheduleService = Depends(get_schedule_service),
    _: User = Depends(get_current_user),
):
    """Get schedule items within the specified date range."""
    return await service.get_range(start, end)


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


@limiter.limit(RateLimits.GROUP_OPERATION)
@router.post("/schedule/copy/group")
async def copy_schedule_by_group(
    request: Request,
    data: ScheduleCopyByGroupRequest,
    repo: ScheduleOperationsRepository = Depends(get_schedule_operation_repository),
    _: User = Depends(require_admin),
) -> None:
    await repo.copy_by_group(
        source_start=data.source_start,
        source_end=data.source_end,
        weeks_to_copy=data.weeks_to_copy,
        group_id=data.group_id,
    )


@limiter.limit(RateLimits.GROUP_OPERATION)
@router.post("/schedule/copy/copy_by_direction")
async def copy_schedule_by_direction(
    request: Request,
    data: ScheduleCopyByDirectionRequest,
    repo: ScheduleOperationsRepository = Depends(get_schedule_operation_repository),
    _: User = Depends(require_admin),
) -> None:
    await repo.copy_by_direction(
        source_start=data.source_start,
        source_end=data.source_end,
        weeks_to_copy=data.weeks_to_copy,
        direction_id=data.direction_id,
    )


@limiter.limit(RateLimits.GROUP_OPERATION)
@router.post("/schedule/delete/group")
async def delete_schedule_by_group(
    request: Request,
    data: ScheduleDeleteByGroupRequest,
    repo: ScheduleOperationsRepository = Depends(
        get_schedule_operation_repository,
    ),
    _: User = Depends(require_admin),
) -> None:
    await repo.delete_by_group(
        start_date=data.start_date,
        weeks_to_delete=data.weeks_to_delete,
        group_id=data.group_id,
    )


@limiter.limit(RateLimits.GROUP_OPERATION)
@router.post("/schedule/delete/direction")
async def delete_schedule_by_direction(
    request: Request,
    data: ScheduleDeleteByDirectionRequest,
    repo: ScheduleOperationsRepository = Depends(
        get_schedule_operation_repository,
    ),
    _: User = Depends(require_admin),
) -> None:
    await repo.delete_by_direction(
        start_date=data.start_date,
        weeks_to_delete=data.weeks_to_delete,
        direction_id=data.direction_id,
    )
