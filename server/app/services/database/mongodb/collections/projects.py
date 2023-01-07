from typing import cast
from datetime import datetime
from bson import ObjectId

from app.services.database.mongodb import MongoDBService, types


def get_projects(
    full: bool = False
) -> list[types.Project]:
    projection = None if full else ['name', 'created_date', 'updated_date']
    return list(MongoDBService.projects().find(projection=projection))


def get_project(
    project_id: ObjectId,
    full: bool = False
) -> types.Project | None:
    projection = None if full else ['name', 'created_date', 'updated_date']
    return MongoDBService.projects().find_one(
        filter={'_id': project_id},
        projection=projection
    )


def create_project(
    name: str
) -> ObjectId:
    result = MongoDBService.projects().insert_one(document=types.Project(
        name=name,
        context_fields=[],
        feature_flags=[],
        updated_date=datetime.utcnow(),
        created_date=datetime.utcnow()
    ))
    return cast(ObjectId, result.inserted_id)


def update_project(
    project_id: ObjectId,
    name: str
) -> bool:
    result = MongoDBService.projects().update_one(
        filter={'_id': project_id},
        update={
            '$set': {
                'name': name,
                'updated_date': datetime.utcnow()
            }
        }
    )
    return result.matched_count > 0


def delete_project(
    project_id: ObjectId
) -> bool:
    result = MongoDBService.projects().delete_one(filter={'_id': project_id})
    return result.deleted_count > 0
