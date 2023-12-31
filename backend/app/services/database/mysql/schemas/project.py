import datetime
from typing import Sequence

from sqlalchemy import String, DateTime, Integer, delete, select, update
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.sql import func, text

from app.services.database.mysql.schemas.base import BaseRow


class ProjectRow(BaseRow):

    __tablename__ = 'projects'

    project_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    private_key: Mapped[str] = mapped_column(String(184))
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.current_timestamp())
    updated_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class ProjectsTable:

    @classmethod
    def get_project_by_name(cls, name: str, session: Session) -> ProjectRow | None:
        return session.scalar(
            select(
                ProjectRow
            ).where(
                ProjectRow.name == name
            )
        )

    @classmethod
    def get_projects(cls, session: Session) -> Sequence[ProjectRow]:
        return session.scalars(
            select(
                ProjectRow
            )
        ).all()

    @staticmethod
    def delete_project(project_id: int, session: Session) -> None:
        session.execute(
            delete(
                ProjectRow
            ).where(
                ProjectRow.project_id == project_id
            )
        )

    @staticmethod
    def update_project(project_id: int, name: str, session: Session) -> None:
        session.execute(
            update(
                ProjectRow
            ).where(
                ProjectRow.project_id == project_id
            ).values({
                ProjectRow.name: name
            })
        )

    @staticmethod
    def update_project_private_key(project_id: int, private_key: str, session: Session) -> None:
        session.execute(
            update(
                ProjectRow
            ).where(
                ProjectRow.project_id == project_id
            ).values({
                ProjectRow.private_key: private_key
            })
        )
