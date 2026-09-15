from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.deps import get_current_user, require_admin
from app.core.rate_limiter import limiter, RateLimits
from app.modules.teachers.dependencies import get_teacher_service
from app.modules.teachers.schemas import (
    TeacherCreate,
    TeacherRead,
    TeacherUpdate,
)
from app.modules.teachers.service import TeacherService
from app.modules.users.models import User

router = APIRouter(prefix="/teachers", tags=["teachers"])


@limiter.limit(RateLimits.READ)
@router.get("/", response_model=List[TeacherRead])
async def list_teachers(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    only_active: bool = False,
    service: TeacherService = Depends(get_teacher_service),
    _: User = Depends(get_current_user),
):
    """Retrieve a list of teachers with pagination and filters."""
    return await service.list_teachers(limit, offset, only_active)


@limiter.limit(RateLimits.READ)
@router.get(
    "/by-discipline/{discipline_id}",
    response_model=List[TeacherRead],
)
async def list_teachers_by_discipline(
    request: Request,
    discipline_id: int,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    only_active: bool = False,
    service: TeacherService = Depends(get_teacher_service),
    _: User = Depends(get_current_user),
):
    """Retrieve a list of teachers associated with a specific discipline."""
    try:
        return await service.list_by_discipline(
            discipline_id, limit, offset, only_active
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.READ)
@router.get("/{teacher_id}", response_model=TeacherRead)
async def get_teacher(
    request: Request,
    teacher_id: int,
    service: TeacherService = Depends(get_teacher_service),
    _: User = Depends(get_current_user),
):
    """Retrieve a specific teacher by their unique identifier."""
    try:
        return await service.get_teacher(teacher_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.post("/", response_model=TeacherRead, status_code=201)
async def create_teacher(
    request: Request,
    data: TeacherCreate,
    service: TeacherService = Depends(get_teacher_service),
    _: User = Depends(require_admin),
):
    """Create a new teacher (admin only)."""
    try:
        return await service.create_teacher(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.patch("/{teacher_id}", response_model=TeacherRead)
async def update_teacher(
    request: Request,
    teacher_id: int,
    data: TeacherUpdate,
    service: TeacherService = Depends(get_teacher_service),
    _: User = Depends(require_admin),
):
    """Update an existing teacher (admin only)."""
    try:
        return await service.update_teacher(teacher_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@limiter.limit(RateLimits.WRITE)
@router.delete("/{teacher_id}", status_code=204)
async def delete_teacher(
    request: Request,
    teacher_id: int,
    service: TeacherService = Depends(get_teacher_service),
    _: User = Depends(require_admin),
):
    """Delete a teacher by their unique identifier (admin only)."""
    try:
        await service.delete_teacher(teacher_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
