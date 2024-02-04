from fastapi import status

from app.services.strings.service import StringsService


class AppException(Exception):
    STATUS: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    CODE: str = 'UNKNOWN'

    def __init__(self, message: str | None = None):
        message = message or StringsService.get(key=self.CODE)
        super().__init__(message)


class NotFoundException(AppException):
    STATUS: int = status.HTTP_404_NOT_FOUND
    CODE: str = 'NOT_FOUND'


class UnauthenticatedException(AppException):
    STATUS: int = status.HTTP_401_UNAUTHORIZED
    CODE: str = 'UNAUTHENTICATED'


class UnauthorizedException(AppException):
    STATUS: int = status.HTTP_403_FORBIDDEN
    CODE: str = 'UNAUTHORIZED'


class BadRequestException(AppException):
    STATUS: int = status.HTTP_400_BAD_REQUEST


class BadRequestFieldException(BadRequestException):
    def __init__(self, field: str, message: str | None = None):
        self.field = field
        super().__init__(message)


class AggregateException(BadRequestException):
    def __init__(self, exceptions: list[AppException]):
        self.exceptions = exceptions
