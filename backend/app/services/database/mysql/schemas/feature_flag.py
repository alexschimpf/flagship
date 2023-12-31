import datetime
from typing import Any, Sequence

import ujson
from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, Text, select, delete, update
from sqlalchemy.orm import Mapped, mapped_column, validates, Session
from sqlalchemy.sql import func, text

from app.services.database.mysql.exceptions.exceptions import ValidationException, ErrorCode
from app.services.database.mysql.schemas.base import BaseRow


class FeatureFlagRow(BaseRow):

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


class FeatureFlagsTable:

    @classmethod
    def get_feature_flags(cls, project_id: int, session: Session) -> Sequence[FeatureFlagRow]:
        return session.scalars(
            select(
                FeatureFlagRow
            ).where(
                FeatureFlagRow.project_id == project_id
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
            FeatureFlagRow.name == name,
            FeatureFlagRow.project_id == project_id
        ]
        if feature_flag_id is not None:
            where_conditions.append(
                FeatureFlagRow.feature_flag_id != feature_flag_id
            )

        stmt = select(
            text('1')
        ).select_from(
            FeatureFlagRow
        ).where(
            *where_conditions
        ).limit(1)

        row = session.scalar(stmt)
        return bool(row)

    @staticmethod
    def delete_feature_flag(project_id: int, feature_flag_id: int, session: Session) -> None:
        session.execute(
            delete(
                FeatureFlagRow
            ).where(
                FeatureFlagRow.project_id == project_id,
                FeatureFlagRow.feature_flag_id == feature_flag_id
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
                FeatureFlagRow
            ).where(
                FeatureFlagRow.feature_flag_id == feature_flag_id,
                FeatureFlagRow.project_id == project_id
            ).values({
                FeatureFlagRow.name: name,
                FeatureFlagRow.description: description,
                FeatureFlagRow.enabled: enabled,
                FeatureFlagRow.conditions: conditions
            })
        )
