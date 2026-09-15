import bcrypt
import hashlib
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from starlette import status

from passlib.context import CryptContext

from app.core.config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


MAX_PASSWORD_LEN = 1024


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    Uses SHA-256 first to avoid the 72-byte bcrypt limit.
    """

    if not password:
        raise ValueError("Password cannot be empty")

    sha256_hash = hashlib.sha256(
        password.encode("utf-8")
    ).digest()

    hashed = bcrypt.hashpw(
        sha256_hash,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain password against a bcrypt hash.
    """

    if not plain_password or not hashed_password:
        return False

    sha256_hash = hashlib.sha256(
        plain_password.encode("utf-8")
    ).digest()

    try:
        return bcrypt.checkpw(
            sha256_hash,
            hashed_password.encode("utf-8")
        )

    except ValueError:
        return False


def get_password_hash(password: str) -> str:
    """
    Compatibility wrapper.
    """
    return hash_password(password)


def create_access_token(
    data: dict,
    expires_delta: int | None = None
) -> str:
    """
    Create JWT access token.
    """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + timedelta(
            minutes=expires_delta
        )
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str):

    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )