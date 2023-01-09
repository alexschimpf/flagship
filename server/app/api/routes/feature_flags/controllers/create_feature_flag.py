from typing import Any
from bson import ObjectId

from app.services.database.mongodb import types, collections
from app.api.routes.feature_flags import schemas
from app.api import exceptions


def process(
    project_id: str,
    request: schemas.CreateOrUpdateFeatureFlag
) -> Any:
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
