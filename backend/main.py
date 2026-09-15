from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings
from app.core.rate_limiter import setup_rate_limiter

from app.core import models_registry  # noqa: F401

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.directions.router import router as directions_router
from app.modules.groups.router import router as groups_router
from app.modules.profiles.router import router as profiles_router
from app.modules.teachers.router import router as teachers_router
from app.modules.disciplines.router import router as disciplines_router
from app.modules.locations.buildings.router import router as buildings_router
from app.modules.locations.rooms.router import router as rooms_router
from app.modules.schedule.router import router as schedule_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage FastAPI application lifespan events."""
    yield


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware that injects secure HTTP headers into responses."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Process the request and attach security headers to the response."""
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        return response


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
    redirect_slashes=False,
    docs_url="/docs" if settings.ENABLE_API_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_API_DOCS else None,
    openapi_url="/openapi.json" if settings.ENABLE_API_DOCS else None,
)


app.add_middleware(SecurityHeadersMiddleware)

setup_rate_limiter(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(directions_router)
app.include_router(groups_router)
app.include_router(profiles_router)
app.include_router(teachers_router)
app.include_router(disciplines_router)
app.include_router(buildings_router)
app.include_router(rooms_router)
app.include_router(schedule_router)


@app.get("/health", include_in_schema=False)
async def health() -> dict:
    """Check application health status."""
    return {"status": "ok"}
