import datetime
from typing import cast

from sqlalchemy import String, DateTime, Integer, ForeignKey, Text, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.services.database.mysql.schemas.base import BaseRow
from app.services.database.mysql.service import MySQLService


class ContextFieldAuditLogRow(BaseRow):

    __tablename__ = 'context_field_audit_logs'

    audit_log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    context_field_id: Mapped[int] = mapped_column(Integer, ForeignKey('context_fields.context_field_id'))
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.project_id'))
    actor: Mapped[str] = mapped_column(String(320))
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(256))
    enum_def: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.current_timestamp())


class ContextFieldAuditLogsTable:

    @staticmethod
    def get_context_field_audit_logs(
        project_id: int,
        context_field_id: int,
        page: int,
        page_size: int
    ) -> tuple[list[ContextFieldAuditLogRow], int]:
        with MySQLService.get_session() as session:
            rows = list(session.scalars(
                select(
                    ContextFieldAuditLogRow
                ).where(
                    ContextFieldAuditLogRow.context_field_id == context_field_id,
                    ContextFieldAuditLogRow.project_id == project_id
                ).order_by(
                    ContextFieldAuditLogRow.created_date.asc()
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
                    ContextFieldAuditLogRow
                ).where(
                    ContextFieldAuditLogRow.project_id == project_id,
                    ContextFieldAuditLogRow.context_field_id == context_field_id
                )
            ))

        return rows, total_count
