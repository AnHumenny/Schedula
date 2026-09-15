class AppException(Exception):
    """Base application exception"""
    pass


class NotFoundError(AppException):
    """Exception: resource not found"""
    pass


class PermissionError(AppException):
    """Exception: insufficient permissions"""
    pass


class ValidationError(AppException):
    """Exception: validation error"""
    pass


class ConflictError(AppException):
    """Exception: data conflict"""
    pass


class AuthenticationError(AppException):
    """Exception: authentication error"""
    pass