from typing import Any
from bson import ObjectId

from app.services.database.mongodb import collections
from app.api import exceptions


def process(
    project_id: str,
    feature_flag_id: str
) -> Any:
    feature_flag = collections.projects.get_feature_flag(
        project_id=ObjectId(project_id), feature_flag_id=ObjectId(feature_flag_id)
    )
    if not feature_flag:
        raise exceptions.NotFoundException

    return feature_flag
