import datetime

from sqlalchemy import String, DateTime, Integer, ForeignKey, Text, Boolean
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.services.database.mysql.schemas.base import BaseRow
from app.services.database.mysql.service import MySQLService


class FeatureFlagAuditLogRow(BaseRow):

    __tablename__ = 'feature_flag_audit_logs'

    audit_log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    feature_flag_id: Mapped[int] = mapped_column(Integer, ForeignKey('feature_flags.feature_flag_id'))
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.project_id'))
    actor: Mapped[str] = mapped_column(String(320))
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(256))
    conditions: Mapped[str] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.current_timestamp())


class FeatureFlagAuditLogsTable:

    @staticmethod
    def get_feature_flag_audit_logs(project_id: int, feature_flag_id: int) -> list[FeatureFlagAuditLogRow]:
        with MySQLService.get_session() as session:
            return list(session.scalars(
                select(
                    FeatureFlagAuditLogRow
                ).where(
                    FeatureFlagAuditLogRow.feature_flag_id == feature_flag_id,
                    FeatureFlagAuditLogRow.project_id == project_id
                ).order_by(
                    FeatureFlagAuditLogRow.created_date.asc()
                )
            ))
