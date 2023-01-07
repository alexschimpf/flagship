from datetime import datetime
from bson import ObjectId

from app.services.database.mongodb import MongoDBService, types


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
                'context_fields.$[el].description': description
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
