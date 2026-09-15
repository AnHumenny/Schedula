import enum


class UserRole(str, enum.Enum):
    """Enumeration of available user roles for access control."""

    ADMIN = "ADMIN"
    USER = "USER"
