import contextlib
import secrets
from bson import ObjectId
from typing import Generator

from app.services.database.mongodb import collections, types


@contextlib.contextmanager
def new_project(
    name: str
) -> Generator[ObjectId, None, None]:
    project_id = None
    try:
        project_id = collections.projects.create_project(
            name=name,
            private_key=secrets.token_hex()
        )
        yield project_id
    finally:
        if project_id:
            collections.projects.delete_project(project_id=project_id)


@contextlib.contextmanager
def new_context_field(
    project_id: ObjectId,
    name: str,
    key: str,
    value_type: types.ContextValueType,
    description: str,
    enum_def: str | None = None
) -> Generator[ObjectId, None, None]:
    context_field_id = None
    try:
        context_field_id, _ = collections.projects.create_context_field(
            project_id=ObjectId(project_id),
            name=name,
            key=key,
            value_type=value_type,
            description=description,
            enum_def=enum_def
        )
        yield context_field_id
    finally:
        if context_field_id:
            collections.projects.delete_context_field(
                project_id=ObjectId(project_id), context_field_id=ObjectId(context_field_id))


@contextlib.contextmanager
def new_feature_flag(
    project_id: ObjectId,
    name: str,
    description: str,
    enabled: bool,
    conditions: list[list[types.FeatureFlagCondition]]
) -> Generator[ObjectId, None, None]:
    feature_flag_id = None
    try:
        feature_flag_id, _ = collections.projects.create_feature_flag(
            project_id=ObjectId(project_id),
            name=name,
            description=description,
            enabled=enabled,
            conditions=conditions
        )
        yield feature_flag_id
    finally:
        if feature_flag_id:
            collections.projects.delete_feature_flag(
                project_id=ObjectId(project_id), feature_flag_id=ObjectId(feature_flag_id))


@contextlib.contextmanager
def new_user(
    email: str,
    name: str,
    role: types.UserRole,
    projects: list[ObjectId],
    password_token: str,
    status: types.UserStatus
) -> Generator[ObjectId, None, None]:
    user_id = None
    try:
        user_id = collections.users.create_user(
            email=email,
            name=name,
            role=role,
            projects=projects,
            password_token=password_token,
            status=status
        )
        yield user_id
    finally:
        if user_id:
            collections.users.delete_user(user_id=user_id)
