import re
import six
import math
from typing import Any
from packaging.version import parse as parse_version

from app.api.routes.feature_flags.constants import ContextValueType, Operator


class ConditionChecker:

    @classmethod
    def check(
        cls,
        context_value: Any,
        context_value_type: int,
        operator: int,
        condition_value: Any
    ) -> bool:
        handler_args = {
            'context_value': context_value,
            'operator': operator,
            'condition_value': condition_value
        }
        match context_value_type:
            case ContextValueType.STRING:
                return cls._handle_string(**handler_args)
            case ContextValueType.NUMBER:
                return cls._handle_number(**handler_args)
            case ContextValueType.INTEGER:
                return cls._handle_integer(**handler_args)
            case ContextValueType.BOOLEAN:
                return cls._handle_boolean(**handler_args)
            case ContextValueType.ENUM:
                return cls._handle_enum(**handler_args)
            case ContextValueType.VERSION:
                return cls._handle_version(**handler_args)
            case ContextValueType.STRING_LIST:
                return cls._handle_string_list(**handler_args)
            case ContextValueType.INTEGER_LIST:
                return cls._handle_integer_list(**handler_args)
            case ContextValueType.ENUM_LIST:
                return cls._handle_enum_list(**handler_args)
            case _:
                raise Exception('Unexpected context value type')

    @staticmethod
    def _handle_string(
        context_value: Any,
        operator: int,
        condition_value: Any
    ) -> bool:
        if context_value is None:
            return False
        if not isinstance(context_value, six.string_types):
            raise TypeError('context_value must be a string')

        if operator == Operator.EQUALS:
            return context_value == condition_value
        elif operator == Operator.NOT_EQUALS:
            return context_value != condition_value
        elif operator == Operator.IN_LIST:
            return context_value in (condition_value or ())
        elif operator == Operator.NOT_IN_LIST:
            return context_value not in (condition_value or ())
        elif operator == Operator.MATCHES_REGEX:
            return bool(re.match(condition_value, context_value))
        else:
            raise ValueError('Unsupported operator')

    @staticmethod
    def _handle_number(
        context_value: Any,
        operator: int,
        condition_value: Any
    ) -> bool:
        if context_value is None:
            return False
        if not isinstance(context_value, (int, float)):
            raise TypeError('context_value must be numeric')

        if operator == Operator.EQUALS:
            return math.isclose(context_value, condition_value)
        elif operator == Operator.NOT_EQUALS:
            return not math.isclose(context_value, condition_value)
        elif operator == Operator.LESS_THAN:
            return context_value < condition_value
        elif operator == Operator.LESS_THAN_OR_EQUAL_TO:
            return math.isclose(context_value, condition_value) or context_value < condition_value
        elif operator == Operator.GREATER_THAN:
            return context_value > condition_value
        elif operator == Operator.GREATER_THAN_OR_EQUAL_TO:
            return math.isclose(context_value, condition_value) or context_value > condition_value
        elif operator == Operator.IN_LIST:
            for list_val in (condition_value or ()):
                if math.isclose(context_value, list_val):
                    return True
            return False
        elif operator == Operator.NOT_IN_LIST:
            for list_val in (condition_value or ()):
                if math.isclose(context_value, list_val):
                    return False
            return True
        else:
            raise ValueError('Unsupported operator')

    @classmethod
    def _handle_integer(
        cls,
        context_value: Any,
        operator: int,
        condition_value: Any
    ) -> bool:
        if context_value is None:
            return False
        if not isinstance(context_value, int):
            raise TypeError('context_value must be an integer')

        return cls.handle_number(
            context_value=context_value,
            operator=operator,
            condition_value=condition_value
        )

    @staticmethod
    def _handle_boolean(
        context_value: Any,
        operator: int,
        condition_value: Any
    ) -> bool:
        if context_value is None:
            return False
        if not isinstance(context_value, bool):
            raise TypeError('context_value must be a boolean')

        if operator == Operator.EQUALS:
            return context_value == condition_value
        elif operator == Operator.NOT_EQUALS:
            return context_value != condition_value
        else:
            raise ValueError('Unsupported operator')

    @staticmethod
    def _handle_enum(
        context_value: Any,
        operator: int,
        condition_value: Any
    ) -> bool:
        if context_value is None:
            return False
        if not isinstance(context_value, six.string_types + (int, float)):
            raise TypeError('context_value must be a string, float, or integer')

        if operator == Operator.EQUALS:
            return context_value == condition_value
        elif operator == Operator.NOT_EQUALS:
            return context_value != condition_value
        elif operator == Operator.IN_LIST:
            return context_value in (condition_value or ())
        elif operator == Operator.NOT_IN_LIST:
            return context_value not in (condition_value or ())
        else:
            raise ValueError('Unsupported operator')

    @staticmethod
    def _handle_version(
        context_value: Any,
        operator: int,
        condition_value: Any
    ) -> bool:
        if context_value is None:
            return False
        if not isinstance(context_value, six.string_types):
            raise TypeError('context_value must be a string')

        context_version = parse_version(context_value)
        condition_version = parse_version(condition_value)
        if operator == Operator.EQUALS:
            return context_version == condition_version
        elif operator == Operator.NOT_EQUALS:
            return context_version != condition_version
        elif operator == Operator.GREATER_THAN:
            return context_version > condition_version
        elif operator == Operator.GREATER_THAN_OR_EQUAL_TO:
            return context_version >= condition_version
        elif operator == Operator.LESS_THAN:
            return context_version < condition_version
        elif operator == Operator.LESS_THAN_OR_EQUAL_TO:
            return context_version <= condition_version
        else:
            raise ValueError('Unsupported operator')

    @classmethod
    def _handle_string_list(
        cls,
        context_value: Any,
        operator: int,
        condition_value: Any
    ) -> bool:
        return cls._handle_list(
            context_value=context_value,
            operator=operator,
            condition_value=condition_value,
            list_type=six.string_types
        )

    @classmethod
    def _handle_integer_list(
        cls,
        context_value: Any,
        operator: int,
        condition_value: Any
    ) -> bool:
        return cls._handle_list(
            context_value=context_value,
            operator=operator,
            condition_value=condition_value,
            list_type=int
        )

    @classmethod
    def _handle_enum_list(
        cls,
        context_value: Any,
        operator: int,
        condition_value: Any
    ) -> bool:
        return cls._handle_list(
            context_value=context_value,
            operator=operator,
            condition_value=condition_value,
            list_type=six.string_types + (int,)
        )

    @staticmethod
    def _handle_list(context_value, operator, condition_value, list_type):
        if isinstance(context_value, list):
            for item in context_value:
                if not isinstance(item, list_type):
                    if isinstance(list_type, tuple):
                        valid_types = f'({', '.join(map(lambda x: x.__name__, list_type))})s'
                    else:
                        valid_types = f'{list_type.__name__}s'
                    raise TypeError('context_value must be a list of ' + valid_types)
        else:
            raise TypeError('context_value must be a list')

        if operator == Operator.CONTAINS:
            return condition_value in context_value
        elif operator == Operator.NOT_CONTAINS:
            return condition_value not in context_value
        elif operator == Operator.INTERSECTS:
            return not set(condition_value).isdisjoint(context_value)
        elif operator == Operator.NOT_INTERSECTS:
            return set(condition_value).isdisjoint(context_value)
        else:
            raise ValueError('Unsupported operator')
