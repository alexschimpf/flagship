from typing import Any
from bson import ObjectId

from app.services.database.mongodb import types, collections
from app.api.routes.feature_flags import schemas
from app.api import exceptions


def process(
    project_id: str,
    feature_flag_id: str,
    request: schemas.CreateOrUpdateFeatureFlag
) -> Any:
    matched = collections.projects.update_feature_flag(
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
    if not matched:
        raise exceptions.NotFoundException

    return collections.projects.get_feature_flag(
        project_id=ObjectId(project_id), feature_flag_id=ObjectId(feature_flag_id)
    )
