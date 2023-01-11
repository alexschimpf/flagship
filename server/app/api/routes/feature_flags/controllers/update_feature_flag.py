from typing import Any
from bson import ObjectId
from varname import nameof

from app.services.database.mongodb import types, collections
from app.api.routes.feature_flags import schemas
from app.api import exceptions


def process(
    project_id: str,
    feature_flag_id: str,
    request: schemas.CreateOrUpdateFeatureFlag
) -> Any:
    _validate_exists(project_id=project_id, feature_flag_id=feature_flag_id)

    errors: list[exceptions.AppException] = []
    _validate_name(project_id=project_id, feature_flag_id=feature_flag_id, request=request, errors=errors)

    if errors:
        raise exceptions.AggregateException(exceptions=errors)

    collections.projects.update_feature_flag(
        project_id=ObjectId(project_id),
        feature_flag_id=ObjectId(feature_flag_id),
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

    return collections.projects.get_feature_flag(
        project_id=ObjectId(project_id), feature_flag_id=ObjectId(feature_flag_id)
    )


def _validate_exists(
    project_id: str,
    feature_flag_id: str
) -> None:
    if not collections.projects.get_feature_flag(
        project_id=ObjectId(project_id),
        feature_flag_id=ObjectId(feature_flag_id)
    ):
        raise exceptions.NotFoundException


def _validate_name(
    project_id: str,
    feature_flag_id: str,
    request: schemas.CreateOrUpdateFeatureFlag,
    errors: list[exceptions.AppException]
) -> None:
    if collections.projects.is_feature_flag_name_taken(
        project_id=ObjectId(project_id),
        name=request.name,
        exclude_feature_flag_id=ObjectId(feature_flag_id)
    ):
        errors.append(exceptions.NameTakenException(field=nameof(request.name)))
