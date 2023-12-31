from typing import Any, Self
import datetime
import ujson
from sqlalchemy.sql import func, text
from sqlalchemy import String, DateTime, Integer, ForeignKey, Text, select, update, delete, Sequence
from sqlalchemy.orm import Mapped, mapped_column, validates, Session

from app.services.database.mysql.models.base import BaseModel
from app.services.database.mysql.exceptions.exceptions import ValidationException, ErrorCode
from app.constants import ContextValueType


class ContextFieldModel(BaseModel):

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
    def validate_value_type(self, _, value: int) -> int:
        # TODO: Make sure correct value type is uesd if enum_def is present
        if value not in ContextValueType:
            raise ValidationException(ErrorCode.INVALID_CONTEXT_FIELD_VALUE_TYPE)

        return value

    @validates('enum_def')
    def validate_enum_def(self, _, value: str) -> str:
        try:
            # TODO
            ujson.loads(value)
        except Exception:
            raise ValidationException(ErrorCode.INVALID_CONTEXT_FIELD_ENUM_DEF)

        return value

    @property
    def enum_def_json(self) -> dict[str, Any] | None:
        if self.enum_def in (None, ''):
            return None
        return ujson.loads(self.enum_def)

    @classmethod
    def get_context_fields(cls, project_id: int, session: Session) -> Sequence[Self]:
        return session.scalars(
            select(
                ContextFieldModel
            ).where(
                ContextFieldModel.project_id == project_id
            )
        ).all()

    @staticmethod
    def update_context_field(
        project_id: int,
        context_field_id: int,
        name: str,
        enum_def: str,
        description: str,
        session: Session
    ):
        session.execute(
            update(
                ContextFieldModel
            ).where(
                ContextFieldModel.context_field_id == context_field_id,
                ContextFieldModel.project_id == project_id
            ).values({
                ContextFieldModel.name: name,
                ContextFieldModel.enum_def: enum_def,
                ContextFieldModel.description: description
            })
        )

    @staticmethod
    def delete_context_field(project_id: int, context_field_id: int, session: Session):
        session.execute(
            delete(
                ContextFieldModel
            ).where(
                ContextFieldModel.project_id == project_id,
                ContextFieldModel.context_field_id == context_field_id
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
            ContextFieldModel.name == name,
            ContextFieldModel.project_id == project_id
        ]
        if context_field_id is not None:
            where_conditions.append(
                ContextFieldModel.context_field_id != context_field_id
            )

        stmt = select(
            text('1')
        ).select_from(
            ContextFieldModel
        ).where(
            *where_conditions
        ).limit(1)

        row = session.scalar(stmt)
        return bool(row)

    @staticmethod
    def is_context_field_field_key_taken(
        field_key: str,
        project_id: int,
        session: Session,
        context_field_id: int | None = None
    ) -> bool:
        where_conditions = [
            ContextFieldModel.field_key == field_key,
            ContextFieldModel.project_id == project_id
        ]
        if context_field_id is not None:
            where_conditions.append(
                ContextFieldModel.context_field_id != context_field_id
            )

        stmt = select(
            text('1')
        ).select_from(
            ContextFieldModel
        ).where(
            *where_conditions
        ).limit(1)

        row = session.scalar(stmt)
        return bool(row)
