from enum import IntEnum
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


class UserRole(IntEnum):
    READ_ONLY = 1
    STANDARD = 2
    ADMIN = 3


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
