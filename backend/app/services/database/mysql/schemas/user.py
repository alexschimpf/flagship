import datetime
from typing import cast

import pydantic
from sqlalchemy import String, DateTime, Integer, delete, select, update, Text
from sqlalchemy.orm import Mapped, mapped_column, validates, Session
from sqlalchemy.sql import func, text

from app.constants import UserRole, UserStatus
from app.services.database.mysql.schemas.base import BaseRow


class UserRow(BaseRow):

    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    name: Mapped[str] = mapped_column(String(128))
    role: Mapped[int] = mapped_column(Integer)
    status: Mapped[int] = mapped_column(Integer)
    password: Mapped[str] = mapped_column(String, nullable=True)
    set_password_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.current_timestamp())
    updated_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    @validates('email')
    def validate_email(self, _: str, value: str) -> str:
        try:
            pydantic.validate_email(value)
        except Exception:
            raise ValueError('Invalid email')

        return value

    @validates('role')
    def validate_role(self, _: str, value: int) -> int:
        if value not in UserRole:
            raise ValueError('Invalid role')

        return value

    @validates('status')
    def validate_status(self, _: str, value: int) -> int:
        if value not in UserStatus:
            raise ValueError('Invalid status')

        return value


class UsersTable:

    @staticmethod
    def get_users(page: int, page_size: int, session: Session) -> tuple[list[UserRow], int]:
        rows = list(session.scalars(
            select(
                UserRow
            ).order_by(
                UserRow.email
            ).offset(
                page * page_size
            ).limit(
                page_size
            )
        ))
        total_count = cast(int, session.scalar(
            select(
                func.count()
            ).select_from(
                UserRow
            )
        ))

        return rows, total_count

    @staticmethod
    def delete_user(user_id: int, session: Session) -> None:
        session.execute(
            delete(
                UserRow
            ).where(
                UserRow.user_id == user_id
            )
        )

    @staticmethod
    def update_set_password_token(email: str, set_password_token: str, session: Session) -> None:
        session.execute(
            update(
                UserRow
            ).where(
                UserRow.email == email
            ).values({
                UserRow.set_password_token: set_password_token
            })
        )

    @staticmethod
    def update_password(user_id: int, password: str, session: Session) -> None:
        session.execute(
            update(
                UserRow
            ).where(
                UserRow.user_id == user_id
            ).values({
                UserRow.set_password_token: None,
                UserRow.password: password,
                UserRow.status: UserStatus.ACTIVATED.value
            })
        )

    @staticmethod
    def get_user_by_email(email: str, session: Session) -> UserRow | None:
        return session.scalar(
            select(
                UserRow
            ).where(
                UserRow.email == email
            )
        )

    @staticmethod
    def update_user(user_id: int, name: str, role: int, session: Session) -> None:
        session.execute(
            update(
                UserRow
            ).where(
                UserRow.user_id == user_id
            ).values({
                UserRow.name: name,
                UserRow.role: role
            })
        )
