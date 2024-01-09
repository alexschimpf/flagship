import datetime

from sqlalchemy import String, DateTime, Integer, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.services.database.mysql.schemas.base import BaseRow
from app.services.database.mysql.service import MySQLService


class SystemAuditLogRow(BaseRow):

    __tablename__ = 'system_audit_logs'

    audit_log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor: Mapped[str] = mapped_column(String(320))
    event_type: Mapped[int] = mapped_column(Integer)
    details: Mapped[str | None] = mapped_column(String(300), nullable=True)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.current_timestamp())


class SystemAuditLogsTable:

    @staticmethod
    def get_system_audit_logs() -> list[SystemAuditLogRow]:
        with MySQLService.get_session() as session:
            return list(session.scalars(
                select(
                    SystemAuditLogRow
                ).order_by(
                    SystemAuditLogRow.created_date.desc()
                )
            ))