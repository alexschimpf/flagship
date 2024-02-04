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


class NameTakenException(BadRequestFieldException):
    CODE: str = 'NAME_TAKEN'


class EmailTakenException(BadRequestFieldException):
    CODE: str = 'EMAIL_TAKEN'


class ContextFieldKeyTakenException(BadRequestFieldException):
    CODE: str = 'CONTEXT_FIELD_KEY_TAKEN'


class InvalidEnumDefException(BadRequestFieldException):
    CODE: str = 'INVALID_ENUM_DEF'


class EnumContextFieldTypeWithoutEnumDefException(BadRequestFieldException):
    CODE: str = 'ENUM_CONTEXT_FIELD_TYPE_WITHOUT_ENUM_DEF'


class SameContextFieldKeysInAndGroup(BadRequestFieldException):
    CODE: str = 'SAME_CONTEXT_FIELD_KEYS_IN_AND_GROUP'


class InvalidFeatureFlagConditions(BadRequestFieldException):
    CODE: str = 'INVALID_FEATURE_FLAG_CONDITIONS'


class InvalidProjectException(BadRequestFieldException):
    CODE: str = 'INVALID_PROJECT'


class InvalidPasswordException(BadRequestFieldException):
    CODE: str = 'INVALID_PASSWORD'


class InvalidSetPasswordTokenException(BadRequestException):
    CODE: str = 'INVALID_SET_PASSWORD_TOKEN'


class PasswordsDontMatchException(BadRequestException):
    CODE: str = 'PASSWORDS_DONT_MATCH'


class InvalidLoginCredentialsException(BadRequestException):
    CODE: str = 'INVALID_LOGIN_CREDENTIALS'


class ContextFieldInUseException(BadRequestException):
    CODE: str = 'CONTEXT_FIELD_IN_USE'


class NoProjectAssignedException(BadRequestFieldException):
    CODE: str = 'NO_PROJECT_ASSIGNED'


class NoOwnersLeftException(BadRequestException):
    CODE: str = 'NO_OWNERS_LEFT'


class UserNotActivatedException(BadRequestException):
    CODE: str = 'USER_NOT_ACTIVATED'


class IllegalContextFieldEnumChangeException(BadRequestException):
    CODE: str = 'ILLEGAL_CONTEXT_FIELD_ENUM_CHANGE'
