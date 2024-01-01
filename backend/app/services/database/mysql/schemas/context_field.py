import datetime
from typing import Any

import ujson
from sqlalchemy import String, DateTime, Integer, ForeignKey, Text, select, update, delete
from sqlalchemy.orm import Mapped, mapped_column, validates, Session
from sqlalchemy.sql import func, text

from app.constants import ContextValueType
from app.services.database.mysql.schemas.base import BaseRow


class ContextFieldRow(BaseRow):

    __tablename__ = 'context_fields'

    context_field_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.project_id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(256))
    field_key: Mapped[str] = mapped_column(String(64))
    value_type: Mapped[int] = mapped_column(Integer, default=False)
    enum_def: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.current_timestamp())
    updated_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    @validates('value_type')
    def validate_value_type(self, _: str, value: int) -> int:
        # TODO: Make sure correct value type is uesd if enum_def is present
        if value not in ContextValueType:
            raise ValueError('Invalid value type')

        return value

    @validates('enum_def')
    def validate_enum_def(self, _: str, value: str) -> str:
        try:
            ujson.loads(value)
        except Exception:
            raise ValueError('Invalid enum def')

        return value

    @property
    def enum_def_json(self) -> dict[str, Any] | None:
        if self.enum_def in (None, ''):
            return None
        return ujson.loads(self.enum_def)  # type: ignore


class ContextFieldsTable:

    @staticmethod
    def get_context_fields(project_id: int, session: Session) -> list[ContextFieldRow]:
        return list(session.scalars(
            select(
                ContextFieldRow
            ).where(
                ContextFieldRow.project_id == project_id
            )
        ))

    @staticmethod
    def update_context_field(
        project_id: int,
        context_field_id: int,
        name: str,
        enum_def: str | None,
        description: str,
        session: Session
    ) -> None:
        session.execute(
            update(
                ContextFieldRow
            ).where(
                ContextFieldRow.context_field_id == context_field_id,
                ContextFieldRow.project_id == project_id
            ).values({
                ContextFieldRow.name: name,
                ContextFieldRow.enum_def: enum_def,
                ContextFieldRow.description: description
            })
        )

    @staticmethod
    def delete_context_field(project_id: int, context_field_id: int, session: Session) -> None:
        session.execute(
            delete(
                ContextFieldRow
            ).where(
                ContextFieldRow.project_id == project_id,
                ContextFieldRow.context_field_id == context_field_id
            )
        )

    @staticmethod
    def is_context_field_name_taken(
        name: str,
        project_id: int,
        session: Session,
        context_field_id: int | None = None
    ) -> bool:
        where_conditions = [
            ContextFieldRow.name == name,
            ContextFieldRow.project_id == project_id
        ]
        if context_field_id is not None:
            where_conditions.append(
                ContextFieldRow.context_field_id != context_field_id
            )

        return bool(session.scalar(
            select(
                text('1')
            ).select_from(
                ContextFieldRow
            ).where(
                *where_conditions
            ).limit(1)
        ))

    @staticmethod
    def is_context_field_field_key_taken(
        field_key: str,
        project_id: int,
        session: Session,
        context_field_id: int | None = None
    ) -> bool:
        where_conditions = [
            ContextFieldRow.field_key == field_key,
            ContextFieldRow.project_id == project_id
        ]
        if context_field_id is not None:
            where_conditions.append(
                ContextFieldRow.context_field_id != context_field_id
            )

        return bool(session.scalar(
            select(
                text('1')
            ).select_from(
                ContextFieldRow
            ).where(
                *where_conditions
            ).limit(1)
        ))
