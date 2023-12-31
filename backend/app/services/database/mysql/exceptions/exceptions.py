from enum import Enum


class ErrorCode(Enum):
    INVALID_FEATURE_FLAG_CONDITIONS = 1
    INVALID_CONTEXT_FIELD_VALUE_TYPE = 2
    INVALID_CONTEXT_FIELD_ENUM_DEF = 3
    INVALID_EMAIL = 4
    INVALID_USER_ROLE = 5
    INVALID_USER_STATUS = 6
    INVALID_USER_PROJECTS = 7


class ValidationException(Exception):

    def __init__(self, error_code: ErrorCode):
        self.error_code = error_code
