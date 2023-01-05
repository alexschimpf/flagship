from fastapi import status


class AppException(Exception):
    STATUS: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    CODE: str = 'UNKNOWN'
    DEFAULT_MESSAGE: str = 'Oops, something went wrong!'

    def __init__(self, message: str | None = None):
        message = add_missing_punctuation(message or self.DEFAULT_MESSAGE)
        super().__init__(message)


class NotFoundException(AppException):
    STATUS: int = status.HTTP_404_NOT_FOUND
    CODE: str = 'NOT_FOUND'
    DEFAULT_MESSAGE: str = 'Resource not found'


class UnauthenticatedException(AppException):
    STATUS: int = status.HTTP_401_UNAUTHORIZED
    CODE: str = 'UNAUTHENTICATED'
    DEFAULT_MESSAGE: str = 'You are not authorized to perform this action'


class UnauthorizedException(AppException):
    STATUS: int = status.HTTP_403_FORBIDDEN
    CODE: str = 'UNAUTHORIZED'
    DEFAULT_MESSAGE: str = UnauthenticatedException.DEFAULT_MESSAGE


class BadRequestException(AppException):
    STATUS: int = status.HTTP_400_BAD_REQUEST


class BadRequestFieldException(BadRequestException):
    def __init__(self, field: str, message: str | None = None):
        self.field = field
        super().__init__(message)


class AggregateException(BadRequestException):
    def __init__(self, exceptions: list[AppException]):
        self.exceptions = exceptions


def add_missing_punctuation(message: str) -> str:
    if message and message[-1] not in ('.', '?', '!'):
        message += '.'
    return message
