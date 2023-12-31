import datetime
from typing import Sequence

import pydantic
from sqlalchemy import String, DateTime, Integer, delete, select, update
from sqlalchemy.orm import Mapped, mapped_column, validates, Session
from sqlalchemy.sql import func, text

from app.constants import UserRole, UserStatus
from app.services.database.mysql.exceptions.exceptions import ValidationException, ErrorCode
from app.services.database.mysql.models.base import BaseModel


class UserModel(BaseModel):

    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    name: Mapped[str] = mapped_column(String(128))
    role: Mapped[int] = mapped_column(Integer)
    status: Mapped[int] = mapped_column(Integer)
    projects: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String, nullable=True)
    set_password_token: Mapped[str] = mapped_column(String, nullable=True)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.current_timestamp())
    updated_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    @property
    def projects_list(self) -> list[int]:
        # TODO: Deal with deleted projects (or empty list of projects)
        return list(map(int, self.projects.split(',')))

    @validates('email')
    def validate_email(self, _: str, value: str) -> str:
        try:
            pydantic.validate_email(value)
        except Exception:
            raise ValidationException(ErrorCode.INVALID_EMAIL)

        return value

    @validates('role')
    def validate_role(self, _: str, value: int) -> int:
        if value not in UserRole:
            raise ValidationException(ErrorCode.INVALID_USER_ROLE)

        return value

    @validates('status')
    def validate_status(self, _: str, value: int) -> int:
        if value not in UserStatus:
            raise ValidationException(ErrorCode.INVALID_USER_STATUS)

        return value

    @validates('projects')
    def validate_projects(self, _: str, value: str) -> str:
        try:
            list(map(int, value.split(',')))
        except Exception:
            raise ValidationException(ErrorCode.INVALID_USER_PROJECTS)

        return value

    @classmethod
    def get_users(cls, session: Session) -> Sequence['UserModel']:
        return session.scalars(
            select(
                UserModel
            )
        ).all()

    @staticmethod
    def delete_user(user_id: int, session: Session) -> None:
        session.execute(
            delete(
                UserModel
            ).where(
                UserModel.user_id == user_id
            )
        )

    @staticmethod
    def update_set_password_token(email: str, set_password_token: str, session: Session) -> None:
        session.execute(
            update(
                UserModel
            ).where(
                UserModel.email == email
            ).values({
                UserModel.set_password_token: set_password_token
            })
        )

    @staticmethod
    def update_password(user_id: int, password: str, session: Session) -> None:
        session.execute(
            update(
                UserModel
            ).where(
                UserModel.user_id == user_id
            ).values({
                UserModel.set_password_token: None,
                UserModel.password: password
            })
        )

    @classmethod
    def get_user_by_email(cls, email: str, session: Session) -> 'UserModel | None':
        return session.scalar(
            select(
                UserModel
            ).where(
                UserModel.email == email
            )
        )

    @classmethod
    def update_user(cls, user_id: int, name: str, role: int, projects: str, session: Session) -> None:
        session.execute(
            update(
                UserModel
            ).where(
                UserModel.user_id == user_id
            ).values({
                UserModel.name: name,
                UserModel.role: role,
                UserModel.projects: projects
            })
        )
