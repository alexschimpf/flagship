from typing import Any
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api.routes.feature_flags import schemas
from app.api import exceptions


def process(
    project_id: str
) -> Any:
    feature_flags = collections.projects.get_feature_flags(project_id=ObjectId(project_id))
    if feature_flags is None:
        raise exceptions.NotFoundException

    feature_flags.sort(key=lambda item: item['name'])

    return schemas.FeatureFlags(items=feature_flags)
