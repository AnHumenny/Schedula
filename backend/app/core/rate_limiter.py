import ipaddress

from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.core.config import settings


def get_real_ip(request: Request) -> str:
    """Real IP address, including proxies."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()

    cf = request.headers.get("CF-Connecting-IP")
    if cf:
        return cf

    return get_remote_address(request)


def is_trusted_ip(ip: str) -> bool:
    """Is the IP address included in the trusted list?"""
    for trusted in settings.trusted_ips_list:
        if "/" in trusted:
            try:
                if ipaddress.ip_address(ip) in ipaddress.ip_network(
                    trusted, strict=False
                ):
                    return True
            except ValueError:
                continue
        elif ip == trusted:
            return True
    return False


def get_user_key(request: Request) -> str:
    """Key for rate limiter: trusted / user:<id> / ip:<ip>."""
    client_ip = get_real_ip(request)

    if is_trusted_ip(client_ip):
        return "trusted"

    user_id = getattr(request.state, "user_id", None)
    if user_id:
        return f"user:{user_id}"

    return f"ip:{client_ip}"


class RateLimits:
    """Structure"""
    AUTH = settings.RATE_LIMIT_AUTH
    WRITE = settings.RATE_LIMIT_WRITE
    READ = settings.RATE_LIMIT_READ
    GROUP_OPERATION = settings.RATE_LIMIT_GROUP_OPERATION
    HEALTH = settings.RATE_LIMIT_HEALTH


REDIS_URL = settings.redis_url_for_limiter

if REDIS_URL and REDIS_URL != "memory://":
    limiter = Limiter(
        key_func=get_user_key,
        storage_uri=REDIS_URL,
        default_limits=[settings.DEFAULT_RATE_LIMIT],
    )
else:
    limiter = Limiter(
        key_func=get_user_key,
        default_limits=[settings.DEFAULT_RATE_LIMIT],
    )


def setup_rate_limiter(app) -> None:
    """Connects slowapi to the application."""

    app.add_middleware(SlowAPIMiddleware)
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Too much requests. Try later"
            },
        )