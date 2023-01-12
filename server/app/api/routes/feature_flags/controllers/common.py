from typing import Any
from bson import ObjectId
from varname import nameof

from app.api import exceptions
from app.api.routes.feature_flags import schemas
from app.api.routes.context_fields.constants import CONTEXT_VALUE_TYPE_OPERATORS
from app.services.database.mongodb import collections, types


def validate_conditions(
    project_id: str,
    request: schemas.CreateOrUpdateFeatureFlag
) -> None:
    conditions = request.conditions
    if not conditions:
        return

    context_fields_by_key = _get_context_fields_by_key(project_id=project_id)
    if not context_fields_by_key:
        # There are conditions but no context fields defined
        raise exceptions.InvalidFeatureFlagConditions(field=nameof(request.conditions))

    for and_group in conditions:
        _validate_and_group(request=request, and_group=and_group)
        for condition in and_group:
            condition.value = _validate_condition(
                condition=condition,
                context_fields_by_key=context_fields_by_key,
                request=request
            )


def _validate_and_group(
    request: schemas.CreateOrUpdateFeatureFlag,
    and_group: list[schemas.FeatureFlagCondition]
) -> None:
    context_keys = set()
    for condition in and_group:
        if condition.context_key in context_keys:
            raise exceptions.SameContextFieldKeysInAndGroup(field=nameof(request.conditions))
        context_keys.add(condition.context_key)


def _validate_condition(
    condition: schemas.FeatureFlagCondition,
    context_fields_by_key: dict[str, types.ContextField],
    request: schemas.CreateOrUpdateFeatureFlag
) -> Any:
    key = condition.context_key
    operator = condition.operator
    value = condition.value

    if key not in context_fields_by_key:
        raise exceptions.InvalidFeatureFlagConditions(field=nameof(request.conditions))

    context_field = context_fields_by_key[key]
    _validate_context_field_and_operator(context_field=context_field, operator=operator, request=request)
    coerced_value = _validate_value(context_field=context_field, operator=operator, value=value, request=request)
    return coerced_value


def _validate_context_field_and_operator(
    context_field: types.ContextField,
    operator: types.Operator,
    request: schemas.CreateOrUpdateFeatureFlag
) -> None:
    value_type = context_field['value_type']
    allowed_operators = CONTEXT_VALUE_TYPE_OPERATORS[value_type]
    if operator not in allowed_operators:
        raise exceptions.InvalidFeatureFlagConditions(field=nameof(request.conditions))


def _validate_value(
    context_field: types.ContextField,
    operator: types.Operator,
    value: Any,
    request: schemas.CreateOrUpdateFeatureFlag
) -> Any:
    if value in ('', None) or isinstance(value, (list, dict)):
        raise Exception()

    coerced_value = None
    value_type = context_field['value_type']
    try:
        match value_type:
            case types.ContextValueType.STRING:
                _validate_string_condition(operator=operator, value=value)
            case types.ContextValueType.INTEGER:
                _validate_integer_condition(operator=operator, value=value)
            case types.ContextValueType.NUMBER:
                _validate_number_condition(operator=operator, value=value)
            case types.ContextValueType.BOOLEAN:
                _validate_boolean_condition(value=value)
            case types.ContextValueType.VERSION:
                _validate_version_condition(value=value)
            case types.ContextValueType.ENUM:
                _validate_enum_condition(operator=operator, value=value)
            case types.ContextValueType.STRING_LIST:
                _validate_string_list_condition(operator=operator, value=value)
            case types.ContextValueType.INTEGER_LIST:
                _validate_integer_list_condition(operator=operator, value=value)
            case types.ContextValueType.ENUM_LIST:
                _validate_enum_list_condition(operator=operator, value=value)
            case _:
                raise Exception('Unexpected value type')
    except Exception:
        raise exceptions.InvalidFeatureFlagConditions(field=nameof(request.conditions))

    return coerced_value


def _validate_string_condition(
    operator: types.Operator,
    value: Any
) -> Any:
    if operator in (types.Operator.IN_LIST, types.Operator.NOT_IN_LIST):
        if not isinstance(value, list):
            raise Exception()
        for i, item in enumerate(value):
            if item in ('', None) or isinstance(item, (list, dict)):
                raise Exception()
            value[i] = str(item)
    else:
        value = str(value)

    return value


def _validate_integer_condition(
    operator: types.Operator,
    value: Any
) -> Any:
    if operator in (types.Operator.IN_LIST, types.Operator.NOT_IN_LIST):
        if not isinstance(value, list):
            raise Exception()
        for i, item in enumerate(value):
            value[i] = int(item)
    else:
        value = int(value)

    return value


def _validate_number_condition(
    operator: types.Operator,
    value: Any
) -> Any:
    if operator in (types.Operator.IN_LIST, types.Operator.NOT_IN_LIST):
        if not isinstance(value, list):
            raise Exception()
        for i, item in enumerate(value):
            try:
                value[i] = int(item)
            except Exception:
                value[i] = float(item)
    else:
        try:
            value = int(value)
        except Exception:
            value = float(value)

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
            raise Exception()
    elif not isinstance(value, bool):
        raise Exception()

    return value


def _validate_version_condition(
    value: Any
) -> Any:
    if not isinstance(value, str):
        raise Exception()

    return value


def _validate_enum_condition(
    operator: types.Operator,
    value: Any
) -> Any:
    # TODO: Validate against actual enum definition
    if operator in (types.Operator.IN_LIST, types.Operator.NOT_IN_LIST):
        if not isinstance(value, list):
            raise Exception()
        for item in value:
            if not isinstance(item, (str, int, float)):
                raise Exception()
    else:
        if not isinstance(value, (str, int, float)):
            raise Exception()

    return value


def _validate_string_list_condition(
    operator: types.Operator,
    value: Any
) -> Any:
    if operator in (types.Operator.INTERSECTS, types.Operator.NOT_INTERSECTS):
        if not isinstance(value, list):
            raise Exception()
        for i, item in enumerate(value):
            if item in ('', None) or isinstance(item, (list, dict)):
                raise Exception()
            value[i] = str(item)
    elif operator in (types.Operator.CONTAINS, types.Operator.NOT_CONTAINS):
        value = str(value)

    return value


def _validate_integer_list_condition(
    operator: types.Operator,
    value: Any
) -> Any:
    if operator in (types.Operator.INTERSECTS, types.Operator.NOT_INTERSECTS):
        if not isinstance(value, list):
            raise Exception()
        for i, item in enumerate(value):
            value[i] = int(item)
    elif operator in (types.Operator.CONTAINS, types.Operator.NOT_CONTAINS):
        value = int(value)

    return value


def _validate_enum_list_condition(
    operator: types.Operator,
    value: Any
) -> Any:
    if operator in (types.Operator.INTERSECTS, types.Operator.NOT_INTERSECTS):
        if not isinstance(value, list):
            raise Exception()
        for item in value:
            if not isinstance(item, (str, int, float)):
                raise Exception()
    elif operator in (types.Operator.CONTAINS, types.Operator.NOT_CONTAINS):
        if not isinstance(value, (str, int, float)):
            raise Exception()

    return value


def _get_context_fields_by_key(
    project_id: str
) -> dict[str, types.ContextField]:
    context_fields = collections.projects.get_context_fields(project_id=ObjectId(project_id))
    context_fields_by_key: dict[str, types.ContextField] = {}
    for context_field in context_fields or []:
        context_fields_by_key[context_field['key']] = context_field

    return context_fields_by_key
