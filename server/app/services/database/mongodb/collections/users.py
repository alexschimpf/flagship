from typing import cast
from datetime import datetime
from bson import ObjectId
import bcrypt

from app.services.database.mongodb import MongoDBService, types


# TODO: Consolidate some of these functions


def get_users() -> list[types.User]:
    return list(MongoDBService.users().find())


def get_user(
    user_id: ObjectId
) -> types.User | None:
    return MongoDBService.users().find_one(
        filter={'_id': user_id}
    )


def get_user_by_email(
    email: str
) -> types.User | None:
    return MongoDBService.users().find_one(
        filter={'email': email}
    )


def is_user_email_taken(
    email: str,
    exclude_project_id: ObjectId
) -> bool:
    user = MongoDBService.users().find_one(
        filter={'email': email}
    )
    return bool(
        user and
        (not exclude_project_id or user['_id'] != exclude_project_id)
    )


def create_user(
    email: str,
    name: str,
    role: types.UserRole,
    projects: list[ObjectId],
    password_token: str,
    status: types.UserStatus
) -> ObjectId:
    result = MongoDBService.users().insert_one(document=types.User(
        email=email,
        name=name,
        role=role,
        projects=projects,
        password_token=password_token,
        status=status,
        password=None,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    ))
    return cast(ObjectId, result.inserted_id)


def update_user(
    user_id: ObjectId,
    name: str,
    role: types.UserRole,
    projects: list[ObjectId]
) -> bool:
    result = MongoDBService.projects().update_one(
        filter={'_id': user_id},
        update={
            '$set': {
                'name': name,
                'role': role,
                'projects': projects,
                'updated_date': datetime.utcnow()
            }
        }
    )
    return result.matched_count > 0


def update_user_password(
    user_id: ObjectId,
    password: str
) -> bool:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(prefix=b'2a'))
    result = MongoDBService.users().update_one(
        filter={'_id': user_id},
        update={
            '$set': {
                'password': hashed_password,
                'updated_date': datetime.utcnow(),
                'password_token': None
            }
        }
    )
    return result.matched_count > 0


def update_user_password_token(
    user_id: ObjectId,
    password_token: str
) -> bool:
    result = MongoDBService.users().update_one(
        filter={'_id': user_id},
        update={
            '$set': {
                'password_token': password_token,
                'updated_date': datetime.utcnow()
            }
        }
    )
    return result.matched_count > 0


def delete_user(
    user_id: ObjectId
) -> bool:
    result = MongoDBService.users().delete_one(
        filter={'_id': user_id}
    )
    return result.deleted_count > 0
