from typing import Any

from sqlalchemy.orm import Session

from app.api import exceptions
from app.api.routes.feature_flags.schemas import FeatureFlagCondition
from app.constants import Operator, ContextValueType, CONTEXT_VALUE_TYPE_OPERATORS
from app.services.database.mysql.schemas.context_field import ContextFieldsTable, ContextFieldRow


def validate_feature_flag_conditions(
    project_id: int,
    conditions: list[list[FeatureFlagCondition]],
    session: Session
) -> None:
    if not conditions:
        return

    context_fields_by_key = _get_context_fields_by_field_key(project_id=project_id, session=session)
    if not context_fields_by_key:
        # There are conditions but no context fields defined
        raise exceptions.InvalidFeatureFlagConditions(field='conditions')

    for and_group in conditions:
        _validate_and_group(and_group=and_group)
        for condition in and_group:
            condition.value = _validate_condition(
                condition=condition,
                context_fields_by_key=context_fields_by_key
            )


def _validate_and_group(
    and_group: list[FeatureFlagCondition]
) -> None:
    context_keys = set()
    for condition in and_group:
        if condition.context_key in context_keys:
            raise exceptions.SameContextFieldKeysInAndGroup(field='conditions')
        context_keys.add(condition.context_key)


def _validate_condition(
    condition: FeatureFlagCondition,
    context_fields_by_key: dict[str, ContextFieldRow]
) -> Any:
    key = condition.context_key
    operator = condition.operator
    value = condition.value

    if key not in context_fields_by_key:
        raise exceptions.InvalidFeatureFlagConditions(field='conditions')

    context_field = context_fields_by_key[key]
    _validate_context_field_and_operator(context_field=context_field, operator=operator)
    coerced_value = _validate_value(context_field=context_field, operator=operator, value=value)
    return coerced_value


def _validate_context_field_and_operator(
    context_field: ContextFieldRow,
    operator: Operator
) -> None:
    value_type = context_field.value_type
    allowed_operators = CONTEXT_VALUE_TYPE_OPERATORS[ContextValueType(value_type)]
    if operator not in allowed_operators:
        raise exceptions.InvalidFeatureFlagConditions(field='conditions')


def _validate_value(
    context_field: ContextFieldRow,
    operator: Operator,
    value: Any
) -> Any:
    if value in ('', None) or isinstance(value, dict):
        raise exceptions.InvalidFeatureFlagConditions(field='conditions')

    coerced_value: Any
    value_type = context_field.value_type
    try:
        match value_type:
            case ContextValueType.STRING:
                coerced_value = _validate_string_condition(operator=operator, value=value)
            case ContextValueType.INTEGER:
                coerced_value = _validate_integer_condition(operator=operator, value=value)
            case ContextValueType.NUMBER:
                coerced_value = _validate_number_condition(operator=operator, value=value)
            case ContextValueType.BOOLEAN:
                coerced_value = _validate_boolean_condition(value=value)
            case ContextValueType.VERSION:
                coerced_value = _validate_version_condition(value=value)
            case ContextValueType.ENUM:
                coerced_value = _validate_enum_condition(operator=operator, value=value)
            case ContextValueType.STRING_LIST:
                coerced_value = _validate_string_list_condition(operator=operator, value=value)
            case ContextValueType.INTEGER_LIST:
                coerced_value = _validate_integer_list_condition(operator=operator, value=value)
            case ContextValueType.ENUM_LIST:
                coerced_value = _validate_enum_list_condition(operator=operator, value=value)
            case _:
                raise Exception('Unexpected value type')
    except Exception:
        raise exceptions.InvalidFeatureFlagConditions(field='conditions')

    return coerced_value


def _validate_string_condition(
    operator: Operator,
    value: Any
) -> Any:
    if operator in (Operator.IN_LIST, Operator.NOT_IN_LIST):
        if not isinstance(value, list):
            raise Exception
        for i, item in enumerate(value):
            if item in ('', None) or isinstance(item, (list, dict)):
                raise Exception
            value[i] = str(item)
    else:
        if isinstance(value, list):
            raise Exception
        value = str(value)

    return value


def _validate_integer_condition(
    operator: Operator,
    value: Any
) -> Any:
    if operator in (Operator.IN_LIST, Operator.NOT_IN_LIST):
        if not isinstance(value, list):
            raise Exception
        for i, item in enumerate(value):
            if isinstance(item, (float, bool)) or (isinstance(item, str) and '.' in item):
                raise Exception
            value[i] = int(item)
    else:
        if isinstance(value, (float, bool)) or (isinstance(value, str) and '.' in value):
            raise Exception
        value = int(value)

    return value


def _validate_number_condition(
    operator: Operator,
    value: Any
) -> Any:
    if operator in (Operator.IN_LIST, Operator.NOT_IN_LIST):
        if not isinstance(value, list):
            raise Exception
        for i, item in enumerate(value):
            try:
                value[i] = float(item)
            except Exception:
                value[i] = int(item)
    else:
        try:
            value = float(value)
        except Exception:
            value = int(value)

    return value


def _validate_boolean_condition(
    value: Any
) -> Any:
    if isinstance(value, str):
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        else:
            raise Exception
    elif not isinstance(value, bool):
        raise Exception

    return value


def _validate_version_condition(
    value: Any
) -> Any:
    if not isinstance(value, str):
        raise Exception

    return value


def _validate_enum_condition(
    operator: Operator,
    value: Any
) -> Any:
    # TODO: Validate against actual enum definition
    if operator in (Operator.IN_LIST, Operator.NOT_IN_LIST):
        if not isinstance(value, list):
            raise Exception
        for item in value:
            if isinstance(item, bool) or not isinstance(item, (str, int, float)):
                raise Exception
    else:
        if isinstance(value, bool) or not isinstance(value, (str, int, float)):
            raise Exception

    return value


def _validate_string_list_condition(
    operator: Operator,
    value: Any
) -> Any:
    if operator in (Operator.INTERSECTS, Operator.NOT_INTERSECTS):
        if not isinstance(value, list):
            raise Exception
        for i, item in enumerate(value):
            if item in ('', None) or isinstance(item, (list, dict)):
                raise Exception
            value[i] = str(item)
    elif operator in (Operator.CONTAINS, Operator.NOT_CONTAINS):
        if isinstance(value, list):
            raise Exception
        value = str(value)

    return value


def _validate_integer_list_condition(
    operator: Operator,
    value: Any
) -> Any:
    if operator in (Operator.INTERSECTS, Operator.NOT_INTERSECTS):
        if not isinstance(value, list):
            raise Exception
        for i, item in enumerate(value):
            if isinstance(item, (float, bool)) or (isinstance(item, str) and '.' in item):
                raise Exception
            value[i] = int(item)
    elif operator in (Operator.CONTAINS, Operator.NOT_CONTAINS):
        if isinstance(value, (float, bool)) or (isinstance(value, str) and '.' in value):
            raise Exception
        value = int(value)

    return value


def _validate_enum_list_condition(
    operator: Operator,
    value: Any
) -> Any:
    if operator in (Operator.INTERSECTS, Operator.NOT_INTERSECTS):
        if not isinstance(value, list):
            raise Exception
        for item in value:
            if isinstance(item, bool) or not isinstance(item, (str, int, float)):
                raise Exception
    elif operator in (Operator.CONTAINS, Operator.NOT_CONTAINS):
        if isinstance(value, bool) or not isinstance(value, (str, int, float)):
            raise Exception

    return value


def _get_context_fields_by_field_key(
    project_id: int,
    session: Session
) -> dict[str, ContextFieldRow]:
    context_fields = ContextFieldsTable.get_context_fields(project_id=project_id, session=session)
    context_fields_by_key: dict[str, ContextFieldRow] = {}
    for context_field in context_fields or []:
        context_fields_by_key[context_field.field_key] = context_field

    return context_fields_by_key
