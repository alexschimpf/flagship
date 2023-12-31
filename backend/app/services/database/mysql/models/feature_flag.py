import datetime
from typing import Any, Sequence

import ujson
from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, Text, select, delete, update
from sqlalchemy.orm import Mapped, mapped_column, validates, Session
from sqlalchemy.sql import func, text

from app.services.database.mysql.exceptions.exceptions import ValidationException, ErrorCode
from app.services.database.mysql.models.base import BaseModel


class FeatureFlagModel(BaseModel):

    __tablename__ = 'feature_flags'

    feature_flag_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.project_id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(256))
    conditions: Mapped[str] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.current_timestamp())
    updated_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    @validates('conditions')
    def validate_conditions(self, _: str, value: str) -> str:
        try:
            ujson.loads(value)
        except Exception:
            raise ValidationException(ErrorCode.INVALID_FEATURE_FLAG_CONDITIONS)

        return value

    @property
    def conditions_json(self) -> list[list[dict[str, Any]]]:
        return ujson.loads(self.conditions)  # type: ignore

    @classmethod
    def get_feature_flags(cls, project_id: int, session: Session) -> Sequence['FeatureFlagModel']:
        return session.scalars(
            select(
                FeatureFlagModel
            ).where(
                FeatureFlagModel.project_id == project_id
            )
        ).all()

    @staticmethod
    def is_feature_flag_name_taken(
        name: str,
        project_id: int,
        session: Session,
        feature_flag_id: int | None = None,
    ) -> bool:
        where_conditions = [
            FeatureFlagModel.name == name,
            FeatureFlagModel.project_id == project_id
        ]
        if feature_flag_id is not None:
            where_conditions.append(
                FeatureFlagModel.feature_flag_id != feature_flag_id
            )

        stmt = select(
            text('1')
        ).select_from(
            FeatureFlagModel
        ).where(
            *where_conditions
        ).limit(1)

        row = session.scalar(stmt)
        return bool(row)

    @staticmethod
    def delete_feature_flag(project_id: int, feature_flag_id: int, session: Session) -> None:
        session.execute(
            delete(
                FeatureFlagModel
            ).where(
                FeatureFlagModel.project_id == project_id,
                FeatureFlagModel.feature_flag_id == feature_flag_id
            )
        )

    @staticmethod
    def update_feature_flag(
        project_id: int,
        feature_flag_id: int,
        name: str,
        description: str,
        enabled: bool,
        conditions: str,
        session: Session
    ) -> None:
        session.execute(
            update(
                FeatureFlagModel
            ).where(
                FeatureFlagModel.feature_flag_id == feature_flag_id,
                FeatureFlagModel.project_id == project_id
            ).values({
                FeatureFlagModel.name: name,
                FeatureFlagModel.description: description,
                FeatureFlagModel.enabled: enabled,
                FeatureFlagModel.conditions: conditions
            })
        )
