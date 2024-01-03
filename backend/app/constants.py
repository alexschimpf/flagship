from enum import IntEnum, auto
from typing import Final


class ContextValueType(IntEnum):
    STRING = 1
    NUMBER = 2
    INTEGER = 3
    BOOLEAN = 4
    ENUM = 5
    VERSION = 6
    STRING_LIST = 7
    INTEGER_LIST = 8
    ENUM_LIST = 9


class Operator(IntEnum):
    EQUALS = 1
    NOT_EQUALS = 2
    LESS_THAN = 3
    LESS_THAN_OR_EQUAL_TO = 4
    GREATER_THAN = 5
    GREATER_THAN_OR_EQUAL_TO = 6
    MATCHES_REGEX = 7
    IN_LIST = 8
    NOT_IN_LIST = 9
    INTERSECTS = 10
    NOT_INTERSECTS = 11
    CONTAINS = 12
    NOT_CONTAINS = 13


class Permission(IntEnum):
    # Projects
    CREATE_PROJECT = auto()
    UPDATE_PROJECT = auto()
    DELETE_PROJECT = auto()
    RESET_PROJECT_PRIVATE_KEY = auto()

    # Feature flags
    CREATE_FEATURE_FLAG = auto()
    UPDATE_FEATURE_FLAG = auto()
    DELETE_FEATURE_FLAG = auto()

    # Context fields
    CREATE_CONTEXT_FIELD = auto()
    UPDATE_CONTEXT_FIELD = auto()
    DELETE_CONTEXT_FIELD = auto()

    # Users
    READ_USERS = auto()
    INVITE_USER = auto()
    UPDATE_USER = auto()
    DELETE_USER = auto()


class UserRole(IntEnum):
    READ_ONLY = 1
    STANDARD = 2
    ADMIN = 3
    OWNER = 4

    def has_permission(self, permission: Permission) -> bool:
        if self is self.STANDARD:
            return permission in (
                Permission.CREATE_FEATURE_FLAG,
                Permission.UPDATE_FEATURE_FLAG,
                Permission.DELETE_FEATURE_FLAG
            )
        elif self is self.ADMIN:
            return permission in (
                Permission.CREATE_FEATURE_FLAG,
                Permission.UPDATE_FEATURE_FLAG,
                Permission.DELETE_FEATURE_FLAG,
                Permission.CREATE_CONTEXT_FIELD,
                Permission.UPDATE_CONTEXT_FIELD,
                Permission.DELETE_CONTEXT_FIELD
            )
        elif self is self.OWNER:
            return True

        return False


class UserStatus(IntEnum):
    INVITED = 1
    ACTIVATED = 2


CONTEXT_VALUE_TYPE_OPERATORS: Final[dict[ContextValueType, set[Operator]]] = {
    ContextValueType.STRING: {
        Operator.EQUALS,
        Operator.NOT_EQUALS,
        Operator.MATCHES_REGEX,
        Operator.IN_LIST,
        Operator.NOT_IN_LIST
    },
    ContextValueType.NUMBER: {
        Operator.EQUALS,
        Operator.NOT_EQUALS,
        Operator.IN_LIST,
        Operator.NOT_IN_LIST,
        Operator.LESS_THAN,
        Operator.LESS_THAN_OR_EQUAL_TO,
        Operator.GREATER_THAN,
        Operator.GREATER_THAN_OR_EQUAL_TO
    },
    ContextValueType.INTEGER: {
        Operator.EQUALS,
        Operator.NOT_EQUALS,
        Operator.IN_LIST,
        Operator.NOT_IN_LIST,
        Operator.LESS_THAN,
        Operator.LESS_THAN_OR_EQUAL_TO,
        Operator.GREATER_THAN,
        Operator.GREATER_THAN_OR_EQUAL_TO
    },
    ContextValueType.BOOLEAN: {
        Operator.EQUALS,
        Operator.NOT_EQUALS
    },
    ContextValueType.ENUM: {
        Operator.EQUALS,
        Operator.NOT_EQUALS,
        Operator.IN_LIST,
        Operator.NOT_IN_LIST
    },
    ContextValueType.VERSION: {
        Operator.EQUALS,
        Operator.NOT_EQUALS,
        Operator.GREATER_THAN,
        Operator.GREATER_THAN_OR_EQUAL_TO,
        Operator.LESS_THAN,
        Operator.LESS_THAN_OR_EQUAL_TO
    },
    ContextValueType.STRING_LIST: {
        Operator.INTERSECTS,
        Operator.NOT_INTERSECTS,
        Operator.CONTAINS,
        Operator.NOT_CONTAINS
    },
    ContextValueType.INTEGER_LIST: {
        Operator.INTERSECTS,
        Operator.NOT_INTERSECTS,
        Operator.CONTAINS,
        Operator.NOT_CONTAINS
    },
    ContextValueType.ENUM_LIST: {
        Operator.INTERSECTS,
        Operator.NOT_INTERSECTS,
        Operator.CONTAINS,
        Operator.NOT_CONTAINS
    }
}
