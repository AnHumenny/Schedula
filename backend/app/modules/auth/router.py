from fastapi import APIRouter, Depends, HTTPException, status, Request

from app.core.deps import get_current_user
from app.core.rate_limiter import limiter, RateLimits
from app.modules.auth.dependencies import get_auth_service
from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.modules.auth.service import AuthService
from app.modules.users.models import User
from app.modules.users.schemas import UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@limiter.limit(RateLimits.AUTH)
@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request,
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Authenticate user and return a JWT access token."""
    identifier = (data.username or data.email or "").strip()
    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username or email is required",
        )

    user = await service.authenticate(identifier, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return TokenResponse(access_token=service.make_token(user))


@limiter.limit(RateLimits.READ)
@router.get("/me", response_model=UserRead)
async def me(
        request: Request,
        current_user: User = Depends(get_current_user),
        ):
    """Return the currently authenticated user."""
    return UserRead.model_validate(current_user)


@limiter.limit(RateLimits.WRITE)
@router.post("/logout", status_code=204)
async def logout(request: Request,):
    """Logout the current user (stateless; client must discard the token)."""
    return None