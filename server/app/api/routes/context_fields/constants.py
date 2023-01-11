from typing import Final

from app.services.database.mongodb.types import Operator, ContextValueType


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
