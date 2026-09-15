from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.deps import get_current_user, require_admin
from app.core.rate_limiter import RateLimits, limiter
from app.modules.disciplines.dependencies import get_discipline_service
from app.modules.disciplines.schemas import (
    DisciplineCreate,
    DisciplineRead,
    DisciplineUpdate,
)
from app.modules.disciplines.service import DisciplineService
from app.modules.users.models import User

router = APIRouter(prefix="/disciplines", tags=["disciplines"])


@limiter.limit(RateLimits.READ)
@router.get("/", response_model=List[DisciplineRead])
async def list_disciplines(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    only_active: bool = False,
    service: DisciplineService = Depends(get_discipline_service),
    _: User = Depends(get_current_user),
):
    """List disciplines with optional active filter and pagination."""
    return await service.list_disciplines(limit, offset, only_active)


@limiter.limit(RateLimits.READ)
@router.get(
    "/by-teacher/{teacher_id}",
    response_model=List[DisciplineRead],
)
async def list_disciplines_by_teacher(
    request: Request,
    teacher_id: int,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    only_active: bool = False,
    service: DisciplineService = Depends(get_discipline_service),
    _: User = Depends(get_current_user),
):
    """List disciplines taught by a specific teacher."""
    try:
        return await service.list_by_teacher(
            teacher_id, limit, offset, only_active
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.READ)
@router.get("/{discipline_id}", response_model=DisciplineRead)
async def get_discipline(
    request: Request,
    discipline_id: int,
    service: DisciplineService = Depends(get_discipline_service),
    _: User = Depends(get_current_user),
):
    """Get a single discipline by ID."""
    try:
        return await service.get_discipline(discipline_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.post("/", response_model=DisciplineRead, status_code=201)
async def create_discipline(
    request: Request,
    data: DisciplineCreate,
    service: DisciplineService = Depends(get_discipline_service),
    _: User = Depends(require_admin),
):
    """Create a new discipline (admin only)."""
    try:
        return await service.create_discipline(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.patch("/{discipline_id}", response_model=DisciplineRead)
async def update_discipline(
    request: Request,
    discipline_id: int,
    data: DisciplineUpdate,
    service: DisciplineService = Depends(get_discipline_service),
    _: User = Depends(require_admin),
):
    """Update an existing discipline (admin only)."""
    try:
        return await service.update_discipline(discipline_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.READ)
@router.delete("/{discipline_id}", status_code=204)
async def delete_discipline(
    request: Request,
    discipline_id: int,
    service: DisciplineService = Depends(get_discipline_service),
    _: User = Depends(require_admin),
):
    """Delete a discipline by ID (admin only)."""
    try:
        await service.delete_discipline(discipline_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
