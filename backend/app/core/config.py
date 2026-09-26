import json
import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


env_file = os.getenv("ENV_SCHEDULER_FILE", ".env")

if Path(env_file).exists():
    load_dotenv(env_file)


class Settings(BaseSettings):
    """Configuration application SCHEDULER API."""

    APP_NAME: str = "SCHEDULER API"
    DEBUG: bool = False
    ENABLE_API_DOCS: bool = True
    PORT: int = 8007

    SECRET_KEY: str = Field(
        ...,
        description="Secret key for JWT signing",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DATABASE_URL: str = Field(
        ...,
        description="Database URL (postgresql+asyncpg://...)",
    )

    ALLOWED_ORIGINS: str = Field(
        default="http://localhost:5174,http://127.0.0.1:5174",
        description="Comma-separated list of allowed CORS origins",
    )

    REDIS_URL: Optional[str] = Field(
        default=None,
        description="Redis URL for rate limiter / cache. If None — memory backend.",
    )

    TRUSTED_IPS: str = Field(
        default="127.0.0.1,172.17.0.1,10.0.0.0/8",
        description="Comma-separated list of trusted IPs (bypass rate limiter)",
    )

    RATE_LIMIT_ENABLED: bool = Field(
        default=True,
        description="Enable rate limiting",
    )
    DEFAULT_RATE_LIMIT: str = Field(
        default="1000/hour",
        description="Default rate limit for all endpoints",
    )
    RATE_LIMIT_AUTH: str = Field(
        default="5/minute",
        description="Rate limit for authentication endpoints",
    )
    RATE_LIMIT_WRITE: str = Field(
        default="30/minute",
        description="Rate limit for write operations",
    )
    RATE_LIMIT_READ: str = Field(
        default="100/minute",
        description="Rate limit for read operations",
    )
    RATE_LIMIT_GROUP_OPERATION: str = Field(
        default="5/minute",
        description="Rate limits for bulk parameter update operations",
    )
    RATE_LIMIT_HEALTH: str = Field(
        default="10/second",
        description="Rate limit for health checks",
    )

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


    @property
    def trusted_ips_list(self) -> List[str]:
        """List of trusted IP."""
        return [
            ip.strip()
            for ip in self.TRUSTED_IPS.split(",")
            if ip.strip()
        ]

    @property
    def allowed_origins_list(self) -> list[str] | None:
        raw = self.ALLOWED_ORIGINS.strip()
        if raw.startswith("["):
            try:
                return [str(x).strip() for x in json.loads(raw)]
            except json.JSONDecodeError:
                pass
        return [o.strip() for o in raw.split(",") if o.strip()]


    @property
    def redis_url_for_limiter(self) -> str:
        """
        URL for rate limiter:
        - if REDIS_URL — use Redis;
        - overwise — memory:// (in-process).
        """
        if not self.REDIS_URL:
            return "memory://"
        return self.REDIS_URL.rstrip("/").rsplit("/", 1)[0] + "/1" \
            if self.REDIS_URL.count("/") >= 3 else self.REDIS_URL + "/1"


settings = Settings()
