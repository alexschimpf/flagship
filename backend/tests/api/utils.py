import contextlib
from typing import Generator, Any

import bcrypt
import ujson
from pydantic import BaseModel, EmailStr
from sqlalchemy import delete

from app.api.routes.feature_flags.schemas import FeatureFlagCondition
from app.constants import UserRole, UserStatus, ContextValueType
from app.services.database.mysql.schemas.context_field import ContextFieldRow
from app.services.database.mysql.schemas.feature_flag import FeatureFlagRow
from app.services.database.mysql.schemas.project import ProjectRow
from app.services.database.mysql.schemas.user import UserRow
from app.services.database.mysql.schemas.user_project import UsersProjectsTable
from app.services.database.mysql.service import MySQLService


class User(BaseModel):
    email: EmailStr = 'test.user@gmail.com'
    name: str = 'Test User'
    role: UserRole = UserRole.OWNER
    projects: list[int] = []
    status: UserStatus = UserStatus.ACTIVATED
    password: str = 'Test123!'
    set_password_token: str | None = None

    @property
    def hashed_password(self) -> str:
        return bcrypt.hashpw(
            self.password.encode(),
            bcrypt.gensalt(prefix=b'2a')
        ).decode()


class Project(BaseModel):
    name: str = 'Project #1'
    private_key: str = 'private_key'


class FeatureFlag(BaseModel):
    name: str = 'Enable some feature'
    description: str = 'This flag enables some feature'
    enabled: bool = True
    conditions: list[list[FeatureFlagCondition]] = []


class ContextField(BaseModel):
    name: str = 'Context Field #1'
    description: str = 'This is a context field'
    field_key: str = 'context_field'
    value_type: ContextValueType = ContextValueType.STRING
    enum_def: dict[str, Any] | None = None


@contextlib.contextmanager
def new_user(user: User) -> Generator[UserRow, None, None]:
    user_row = UserRow(
        email=user.email,
        name=user.name,
        role=user.role.value,
        status=user.status.value,
        password=user.hashed_password,
        set_password_token=user.set_password_token
    )
    try:
        with MySQLService.get_session() as session:
            session.add(user_row)
            session.flush()

            if user.projects:
                UsersProjectsTable.update_user_projects(
                    user_id=user_row.user_id, project_ids=user.projects, session=session)

            session.commit()
            session.refresh(user_row)

        yield user_row
    finally:
        if user_row.user_id:
            with MySQLService.get_session() as session:
                session.execute(
                    delete(
                        UserRow
                    ).where(
                        UserRow.user_id == user_row.user_id
                    )
                )
                session.commit()


@contextlib.contextmanager
def new_project(project: Project) -> Generator[ProjectRow, None, None]:
    project_row = ProjectRow(
        name=project.name,
        private_key=project.private_key
    )
    try:
        with MySQLService.get_session() as session:
            session.add(project_row)
            session.commit()
            session.refresh(project_row)

        yield project_row
    finally:
        if project_row.project_id:
            with MySQLService.get_session() as session:
                session.execute(
                    delete(
                        ProjectRow
                    ).where(
                        ProjectRow.project_id == project_row.project_id
                    )
                )
                session.commit()


@contextlib.contextmanager
def new_feature_flag(project_id: int, feature_flag: FeatureFlag) -> Generator[FeatureFlagRow, None, None]:
    conditions = ujson.dumps([
        [condition.model_dump() for condition in and_group]
        for and_group in feature_flag.conditions
    ])
    feature_flag_row = FeatureFlagRow(
        project_id=project_id,
        name=feature_flag.name,
        description=feature_flag.description,
        conditions=conditions,
        enabled=feature_flag.enabled
    )
    try:
        with MySQLService.get_session() as session:
            session.add(feature_flag_row)
            session.commit()
            session.refresh(feature_flag_row)

        yield feature_flag_row
    finally:
        if feature_flag_row.feature_flag_id:
            with MySQLService.get_session() as session:
                session.execute(
                    delete(
                        FeatureFlagRow
                    ).where(
                        FeatureFlagRow.project_id == feature_flag_row.project_id,
                        FeatureFlagRow.feature_flag_id == feature_flag_row.feature_flag_id
                    )
                )
                session.commit()


@contextlib.contextmanager
def new_context_field(project_id: int, context_field: ContextField) -> Generator[ContextFieldRow, None, None]:
    enum_def = ujson.dumps(context_field.enum_def) if context_field.enum_def else None
    context_field_row = ContextFieldRow(
        project_id=project_id,
        name=context_field.name,
        description=context_field.description,
        field_key=context_field.field_key,
        value_type=context_field.value_type.value,
        enum_def=enum_def
    )
    try:
        with MySQLService.get_session() as session:
            session.add(context_field_row)
            session.commit()
            session.refresh(context_field_row)

        yield context_field_row
    finally:
        if context_field_row.context_field_id:
            with MySQLService.get_session() as session:
                session.execute(
                    delete(
                        ContextFieldRow
                    ).where(
                        ContextFieldRow.project_id == context_field_row.project_id,
                        ContextFieldRow.context_field_id == context_field_row.context_field_id
                    )
                )
                session.commit()


def clear_database() -> None:
    with MySQLService.get_session() as session:
        session.execute(delete(UserRow))
        session.execute(delete(ProjectRow))
        session.commit()
