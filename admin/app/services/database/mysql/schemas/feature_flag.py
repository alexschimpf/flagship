import datetime
from typing import Any, cast

import ujson
from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, select, delete, update
from sqlalchemy.orm import Mapped, mapped_column, validates, Session
from sqlalchemy.sql import func, text
from sqlalchemy_utc import UtcDateTime

from app.services.database.mysql.schemas.base import BaseRow


class FeatureFlagRow(BaseRow):
    __tablename__ = 'feature_flags'

    feature_flag_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.project_id'))
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(256))
    conditions: Mapped[str] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_date: Mapped[datetime.datetime] = mapped_column(UtcDateTime, server_default=func.current_timestamp())
    updated_date: Mapped[datetime.datetime] = mapped_column(
        UtcDateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    )

    @validates('conditions')
    def validate_conditions(self, _: str, value: str) -> str:
        try:
            ujson.loads(value)
        except Exception:
            raise ValueError('Invalid conditions')

        return value

    @property
    def conditions_list(self) -> list[list[dict[str, Any]]]:
        return ujson.loads(self.conditions)  # type: ignore


class FeatureFlagsTable:
    @staticmethod
    def get_feature_flags(
        project_id: int, session: Session, page: int | None = None, page_size: int | None = None
    ) -> tuple[list[FeatureFlagRow], int]:
        stmt = (
            select(FeatureFlagRow)
            .where(FeatureFlagRow.project_id == project_id)
            .order_by(FeatureFlagRow.feature_flag_id)
        )

        if page is not None and page_size is not None:
            stmt = stmt.offset(page * page_size).limit(page_size)

        rows = list(session.scalars(stmt))

        total_count = 0
        if page is not None and page_size is not None:
            total_count = cast(
                int,
                session.scalar(
                    select(func.count()).select_from(FeatureFlagRow).where(FeatureFlagRow.project_id == project_id)
                ),
            )

        return rows, total_count

    @staticmethod
    def is_feature_flag_name_taken(
        name: str, project_id: int, session: Session, feature_flag_id: int | None = None
    ) -> bool:
        where_conditions = [FeatureFlagRow.name == name, FeatureFlagRow.project_id == project_id]
        if feature_flag_id is not None:
            where_conditions.append(FeatureFlagRow.feature_flag_id != feature_flag_id)

        return bool(session.scalar(select(text('1')).select_from(FeatureFlagRow).where(*where_conditions).limit(1)))

    @staticmethod
    def delete_feature_flag(project_id: int, feature_flag_id: int, session: Session) -> None:
        session.execute(
            delete(FeatureFlagRow).where(
                FeatureFlagRow.project_id == project_id, FeatureFlagRow.feature_flag_id == feature_flag_id
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
        session: Session,
    ) -> None:
        session.execute(
            update(FeatureFlagRow)
            .where(FeatureFlagRow.feature_flag_id == feature_flag_id, FeatureFlagRow.project_id == project_id)
            .values(
                {
                    FeatureFlagRow.name: name,
                    FeatureFlagRow.description: description,
                    FeatureFlagRow.enabled: enabled,
                    FeatureFlagRow.conditions: conditions,
                }
            )
        )

    @staticmethod
    def update_feature_flag_status(project_id: int, feature_flag_id: int, enabled: bool, session: Session) -> None:
        session.execute(
            update(FeatureFlagRow)
            .where(FeatureFlagRow.feature_flag_id == feature_flag_id, FeatureFlagRow.project_id == project_id)
            .values({FeatureFlagRow.enabled: enabled})
        )
