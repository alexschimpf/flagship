from typing import Any
from bson import ObjectId
from varname import nameof

from app.services.database.mongodb import types, collections
from app.api.routes.feature_flags import schemas
from app.api.routes.feature_flags.controllers import common
from app.api import exceptions


def process(
    project_id: str,
    request: schemas.CreateOrUpdateFeatureFlag
) -> Any:
    errors: list[exceptions.AppException] = []
    _validate_name(project_id=project_id, request=request, errors=errors)
    _validate_conditions(project_id=project_id, request=request, errors=errors)

    if errors:
        raise exceptions.AggregateException(exceptions=errors)

    feature_flag_id, project_found = collections.projects.create_feature_flag(
        project_id=ObjectId(project_id),
        name=request.name,
        description=request.description,
        enabled=request.enabled,
        conditions=[
            [
                types.FeatureFlagCondition(
                    context_key=condition.context_key,
                    operator=condition.operator,
                    value=condition.value
                )
                for condition in group
            ] for group in request.conditions
        ]
    )
    if not project_found:
        raise exceptions.NotFoundException

    return collections.projects.get_feature_flag(
        project_id=ObjectId(project_id), feature_flag_id=feature_flag_id
    )


def _validate_name(
    project_id: str,
    request: schemas.CreateOrUpdateFeatureFlag,
    errors: list[exceptions.AppException]
) -> None:
    if collections.projects.is_feature_flag_name_taken(
        project_id=ObjectId(project_id),
        name=request.name
    ):
        errors.append(exceptions.NameTakenException(field=nameof(request.name)))


def _validate_conditions(
    project_id: str,
    request: schemas.CreateOrUpdateFeatureFlag,
    errors: list[exceptions.AppException]
) -> None:
    try:
        common.validate_conditions(project_id=project_id, request=request)
    except exceptions.AppException as e:
        errors.append(e)
