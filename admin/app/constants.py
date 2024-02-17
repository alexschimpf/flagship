import sys
from enum import IntEnum, auto
from typing import Final, Any
from pydantic import BaseModel
import inspect


DEFAULT_PAGE_SIZE = sys.maxsize


class OpenAPIIntEnum(IntEnum):
    def __new__(cls, value: Any, doc: Any = None) -> Any:
        self = int.__new__(cls, value)
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: Any, handler: Any) -> Any:
        json_schema = BaseModel.__get_pydantic_json_schema__(core_schema, handler)
        json_schema['x-enum-varnames'] = [v.name for v in cls]
        json_schema['oneOf'] = [{'title': v.name, 'const': v.value, 'description': inspect.getdoc(v)} for v in cls]
        json_schema = handler.resolve_ref_schema(json_schema)
        return json_schema


class ContextValueType(OpenAPIIntEnum):
    STRING = 1
    NUMBER = 2
    INTEGER = 3
    BOOLEAN = 4
    ENUM = 5
    VERSION = 6
    STRING_LIST = 7
    INTEGER_LIST = 8
    ENUM_LIST = 9


class Operator(OpenAPIIntEnum):
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


OPERATOR_DISPLAY_NAMES: Final[dict[Operator, str]] = {
    Operator.EQUALS: 'is',
    Operator.NOT_EQUALS: 'is not',
    Operator.LESS_THAN: '<',
    Operator.LESS_THAN_OR_EQUAL_TO: '<=',
    Operator.GREATER_THAN: '>',
    Operator.GREATER_THAN_OR_EQUAL_TO: '>=',
    Operator.MATCHES_REGEX: 'matches',
    Operator.IN_LIST: 'is one of',
    Operator.NOT_IN_LIST: 'is not one of',
    Operator.INTERSECTS: 'has one of',
    Operator.NOT_INTERSECTS: 'does not have any of',
    Operator.CONTAINS: 'has',
    Operator.NOT_CONTAINS: 'does not have',
}


class Permission(OpenAPIIntEnum):
    # Projects
    CREATE_PROJECT = auto()
    UPDATE_PROJECT = auto()
    DELETE_PROJECT = auto()
    READ_PROJECT_PRIVATE_KEYS = auto()
    EDIT_PROJECT_PRIVATE_KEYS = auto()
    CREATE_PROJECT_PRIVATE_KEY = auto()
    DELETE_PROJECT_PRIVATE_KEY = auto()

    # Feature flags
    CREATE_FEATURE_FLAG = auto()
    UPDATE_FEATURE_FLAG = auto()
    DELETE_FEATURE_FLAG = auto()

    # Context fields
    CREATE_CONTEXT_FIELD = auto()
    UPDATE_CONTEXT_FIELD = auto()
    DELETE_CONTEXT_FIELD = auto()
    READ_CONTEXT_FIELD_AUDIT_LOGS = auto()

    # Users
    READ_USERS = auto()
    INVITE_USER = auto()
    UPDATE_USER = auto()
    UPDATE_USER_PROJECTS = auto()
    DELETE_USER = auto()

    # Admin
    READ_SYSTEM_AUDIT_LOGS = auto()


class UserRole(OpenAPIIntEnum):
    READ_ONLY = 5
    STANDARD = 10
    ADMIN = 15
    OWNER = 20

    def has_permission(self, permission: Permission) -> bool:
        if self is self.STANDARD:
            return permission in (
                Permission.CREATE_FEATURE_FLAG,
                Permission.UPDATE_FEATURE_FLAG,
                Permission.DELETE_FEATURE_FLAG,
                Permission.CREATE_CONTEXT_FIELD,
                Permission.UPDATE_CONTEXT_FIELD,
                Permission.DELETE_CONTEXT_FIELD,
                Permission.READ_CONTEXT_FIELD_AUDIT_LOGS,
            )
        elif self is self.ADMIN:
            return permission in (
                Permission.CREATE_FEATURE_FLAG,
                Permission.UPDATE_FEATURE_FLAG,
                Permission.DELETE_FEATURE_FLAG,
                Permission.CREATE_CONTEXT_FIELD,
                Permission.UPDATE_CONTEXT_FIELD,
                Permission.DELETE_CONTEXT_FIELD,
                Permission.READ_CONTEXT_FIELD_AUDIT_LOGS,
                Permission.CREATE_PROJECT,
                Permission.UPDATE_PROJECT,
                Permission.READ_PROJECT_PRIVATE_KEYS,
                Permission.CREATE_PROJECT_PRIVATE_KEY,
                Permission.EDIT_PROJECT_PRIVATE_KEYS,
                Permission.READ_SYSTEM_AUDIT_LOGS,
                Permission.READ_USERS,
                Permission.INVITE_USER,
                Permission.UPDATE_USER,
                Permission.UPDATE_USER_PROJECTS,
                Permission.DELETE_USER,
            )
        elif self is self.OWNER:
            return True

        return False


class UserStatus(OpenAPIIntEnum):
    INVITED = 1
    ACTIVATED = 2


CONTEXT_VALUE_TYPE_OPERATORS: Final[dict[ContextValueType, set[Operator]]] = {
    ContextValueType.STRING: {
        Operator.EQUALS,
        Operator.NOT_EQUALS,
        Operator.MATCHES_REGEX,
        Operator.IN_LIST,
        Operator.NOT_IN_LIST,
    },
    ContextValueType.NUMBER: {
        Operator.EQUALS,
        Operator.NOT_EQUALS,
        Operator.IN_LIST,
        Operator.NOT_IN_LIST,
        Operator.LESS_THAN,
        Operator.LESS_THAN_OR_EQUAL_TO,
        Operator.GREATER_THAN,
        Operator.GREATER_THAN_OR_EQUAL_TO,
    },
    ContextValueType.INTEGER: {
        Operator.EQUALS,
        Operator.NOT_EQUALS,
        Operator.IN_LIST,
        Operator.NOT_IN_LIST,
        Operator.LESS_THAN,
        Operator.LESS_THAN_OR_EQUAL_TO,
        Operator.GREATER_THAN,
        Operator.GREATER_THAN_OR_EQUAL_TO,
    },
    ContextValueType.BOOLEAN: {Operator.EQUALS, Operator.NOT_EQUALS},
    ContextValueType.ENUM: {Operator.EQUALS, Operator.NOT_EQUALS, Operator.IN_LIST, Operator.NOT_IN_LIST},
    ContextValueType.VERSION: {
        Operator.EQUALS,
        Operator.NOT_EQUALS,
        Operator.GREATER_THAN,
        Operator.GREATER_THAN_OR_EQUAL_TO,
        Operator.LESS_THAN,
        Operator.LESS_THAN_OR_EQUAL_TO,
    },
    ContextValueType.STRING_LIST: {
        Operator.INTERSECTS,
        Operator.NOT_INTERSECTS,
        Operator.CONTAINS,
        Operator.NOT_CONTAINS,
    },
    ContextValueType.INTEGER_LIST: {
        Operator.INTERSECTS,
        Operator.NOT_INTERSECTS,
        Operator.CONTAINS,
        Operator.NOT_CONTAINS,
    },
    ContextValueType.ENUM_LIST: {
        Operator.INTERSECTS,
        Operator.NOT_INTERSECTS,
        Operator.CONTAINS,
        Operator.NOT_CONTAINS,
    },
}


class AuditLogEventType(OpenAPIIntEnum):
    INVITED_USER = 1
    DELETED_USER = 2
    UPDATED_USER = 3
    SET_PASSWORD = 4
    RESET_PASSWORD = 5
    ADDED_PROJECT_PRIVATE_KEY = 6
    CREATED_PROJECT = 7
    DELETED_PROJECT = 8
    CREATED_CONTEXT_FIELD = 9
    DELETED_CONTEXT_FIELD = 10
    CREATED_FEATURE_FLAG = 11
    DELETED_FEATURE_FLAG = 12
    DELETED_PROJECT_PRIVATE_KEY = 13
