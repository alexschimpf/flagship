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


def get_context_fields(
    project_id: ObjectId
) -> list[types.ContextField] | None:
    project = MongoDBService.projects().find_one(
        filter={'_id': project_id},
        projection=['context_fields']
    )
    if not project:
        return None

    return project['context_fields']


def get_context_field(
    project_id: ObjectId,
    context_field_id: ObjectId
) -> types.ContextField | None:
    project = MongoDBService.projects().find_one(
        filter={
            '_id': project_id,
        },
        projection={
            'context_fields': {
                '$elemMatch': {
                    '_id': context_field_id
                }
            }
        }
    )
    if not project or not project['context_fields']:
        return None

    return project['context_fields'][0]


def create_context_field(
    project_id: ObjectId,
    name: str,
    key: str,
    value_type: str,
    description: str,
) -> tuple[ObjectId, bool]:
    context_field = types.ContextField(
        _id=ObjectId(),
        name=name,
        key=key,
        value_type=value_type,
        description=description,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    result = MongoDBService.projects().update_one(
        filter={'_id': project_id},
        update={
            '$push': {
                'context_fields': context_field
            }
        }
    )
    return context_field['_id'], result.modified_count > 0


def update_context_field(
    project_id: ObjectId,
    context_field_id: ObjectId,
    name: str,
    description: str
) -> bool:
    result = MongoDBService.projects().update_one(
        filter={'_id': project_id},
        update={
            '$set': {
                'context_fields.$[el].name': name,
                'context_fields.$[el].description': description,
                'context_fields.$[el].updated_date': datetime.utcnow()
            }
        },
        array_filters=[{
            'el._id': {
                '$eq': context_field_id
            }
        }]
    )
    return result.matched_count > 0


def delete_context_field(
    project_id: ObjectId,
    context_field_id: ObjectId
) -> bool:
    result = MongoDBService.projects().update_one(
        filter={'_id': project_id},
        update={
            '$pull': {
                'context_fields': {
                    '_id': context_field_id
                }
            }
        }
    )
    return result.modified_count > 0


def get_feature_flags(
    project_id: ObjectId
) -> list[types.FeatureFlag] | None:
    project = MongoDBService.projects().find_one(
        filter={'_id': project_id},
        projection=['feature_flags']
    )
    if not project:
        return None

    return project['feature_flags']


def get_feature_flag(
    project_id: ObjectId,
    feature_flag_id: ObjectId
) -> types.FeatureFlag | None:
    project = MongoDBService.projects().find_one(
        filter={
            '_id': project_id,
        },
        projection={
            'feature_flags': {
                '$elemMatch': {
                    '_id': feature_flag_id
                }
            }
        }
    )
    if not project or not project['feature_flags']:
        return None

    return project['feature_flags'][0]


def create_feature_flag(
    project_id: ObjectId,
    name: str,
    description: str,
    enabled: bool,
    conditions: list[list[types.FeatureFlagCondition]]
) -> tuple[ObjectId, bool]:
    feature_flag = types.FeatureFlag(
        _id=ObjectId(),
        name=name,
        description=description,
        enabled=enabled,
        conditions=conditions,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    result = MongoDBService.projects().update_one(
        filter={'_id': project_id},
        update={
            '$push': {
                'feature_flags': feature_flag
            }
        }
    )
    return feature_flag['_id'], result.modified_count > 0


def update_feature_flag(
    project_id: ObjectId,
    feature_flag_id: ObjectId,
    name: str,
    description: str,
    enabled: bool,
    conditions: list[list[types.FeatureFlagCondition]]
) -> bool:
    result = MongoDBService.projects().update_one(
        filter={'_id': project_id},
        update={
            '$set': {
                'feature_flags.$[el].name': name,
                'feature_flags.$[el].description': description,
                'feature_flags.$[el].enabled': enabled,
                'feature_flags.$[el].conditions': conditions,
                'feature_flags.$[el].updated_date': datetime.utcnow()
            }
        },
        array_filters=[{
            'el._id': {
                '$eq': feature_flag_id
            }
        }]
    )
    return result.matched_count > 0


def delete_feature_flag(
    project_id: ObjectId,
    feature_flag_id: ObjectId
) -> bool:
    result = MongoDBService.projects().update_one(
        filter={'_id': project_id},
        update={
            '$pull': {
                'feature_flags': {
                    '_id': feature_flag_id
                }
            }
        }
    )
    return result.modified_count > 0
