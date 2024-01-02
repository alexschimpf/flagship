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


class NameTakenException(BadRequestFieldException):
    CODE: str = 'NAME_TAKEN'
    DEFAULT_MESSAGE: str = 'Sorry, that name is already taken'


class EmailTakenException(BadRequestFieldException):
    CODE: str = 'EMAIL_TAKEN'
    DEFAULT_MESSAGE: str = 'Sorry, that email is already taken'


class ContextFieldKeyTakenException(BadRequestFieldException):
    CODE: str = 'CONTEXT_FIELD_KEY_TAKEN'
    DEFAULT_MESSAGE: str = 'Sorry, that context field key is already being used in this project'


class InvalidEnumDefException(BadRequestFieldException):
    CODE: str = 'INVALID_ENUM_DEF'
    DEFAULT_MESSAGE: str = 'Invalid enum definition'


class EnumContextFieldTypeWithoutEnumDefException(BadRequestFieldException):
    CODE: str = 'ENUM_CONTEXT_FIELD_TYPE_WITHOUT_ENUM_DEF'
    DEFAULT_MESSAGE: str = 'Context fields with "enum" or "enum list" types require an enum definition'


class SameContextFieldKeysInAndGroup(BadRequestFieldException):
    CODE: str = 'SAME_CONTEXT_FIELD_KEYS_IN_AND_GROUP'
    DEFAULT_MESSAGE: str = 'Two of the same context field keys cannot be used in the same AND group'


class InvalidFeatureFlagConditions(BadRequestFieldException):
    CODE: str = 'INVALID_FEATURE_FLAG_CONDITIONS'
    DEFAULT_MESSAGE: str = 'Invalid conditions'


class InvalidProjectException(BadRequestFieldException):
    CODE: str = 'INVALID_PROJECT'
    DEFAULT_MESSAGE: str = 'Invalid project'


class InvalidPasswordException(BadRequestFieldException):
    CODE: str = 'INVALID_PASSWORD_EXCEPTION'
    DEFAULT_MESSAGE: str = 'Invalid password. Please see requirements.'


class InvalidLoginCredentialsException(BadRequestException):
    CODE: str = 'INVALID_LOGIN_CREDENTIALS'
    DEFAULT_MESSAGE: str = 'Sorry, the credentials provided are invalid'


class ContextFieldInUseException(BadRequestException):
    CODE: str = 'CONTEXT_FIELD_IN_USE'
    DEFAULT_MESSAGE: str = ('This context field cannot be deleted because it is currently being '
                            'referenced by one or more feature flags')


class NoProjectAssignedException(BadRequestFieldException):
    CODE: str = 'NO_PROJECT_ASSIGNED'
    DEFAULT_MESSAGE: str = 'This user must be assigned to at least one project'


def add_missing_punctuation(message: str) -> str:
    if message and message[-1] not in ('.', '?', '!'):
        message += '.'
    return message
