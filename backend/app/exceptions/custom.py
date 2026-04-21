"""Custom exception classes for the Airbnb Clone API."""

from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Resource", identifier: str | int | None = None):
        detail = f"{resource} not found"
        if identifier is not None:
            detail = f"{resource} with id '{identifier}' not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnauthorizedException(HTTPException):
    """Raised when authentication is required but not provided or invalid."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(HTTPException):
    """Raised when an authenticated user lacks permission for an operation."""

    def __init__(self, message: str = "You do not have permission to perform this action"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)


class ConflictException(HTTPException):
    """Raised on unique constraint violations or duplicate resources."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=message)


class BadRequestException(HTTPException):
    """Raised for malformed or invalid requests."""

    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class PaymentException(HTTPException):
    """Raised when a payment operation fails."""

    def __init__(self, message: str = "Payment processing failed"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=message
        )


class RoomNotAvailableException(BadRequestException):
    """Raised when trying to book an unavailable room."""

    def __init__(self) -> None:
        super().__init__("Room is not available for the selected dates")
