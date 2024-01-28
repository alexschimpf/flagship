import datetime

from sqlalchemy import String, Integer, delete, select, update
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.sql import func, text
from sqlalchemy_utc import UtcDateTime

from app.services.database.mysql.schemas.base import BaseRow


class ProjectRow(BaseRow):

    __tablename__ = 'projects'

    project_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    created_date: Mapped[datetime.datetime] = mapped_column(UtcDateTime, server_default=func.current_timestamp())
    updated_date: Mapped[datetime.datetime] = mapped_column(
        UtcDateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class ProjectsTable:

    @staticmethod
    def get_project_by_name(name: str, session: Session) -> ProjectRow | None:
        return session.scalar(
            select(
                ProjectRow
            ).where(
                ProjectRow.name == name
            )
        )

    @staticmethod
    def get_projects(
        project_ids: list[int],
        page: int,
        page_size: int,
        session: Session
    ) -> tuple[list[ProjectRow], int]:
        rows = list(session.scalars(
            select(
                ProjectRow
            ).where(
                ProjectRow.project_id.in_(project_ids)
            ).order_by(
                ProjectRow.project_id
            ).offset(
                page * page_size
            ).limit(
                page_size
            )
        ))

        return rows, len(project_ids)

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
    def are_projects_valid(project_ids: list[int], session: Session) -> bool:
        all_project_ids = set(
            session.scalars(
                select(
                    ProjectRow.project_id
                )
            ) or ()
        )
        for project_id in project_ids:
            if project_id not in all_project_ids:
                return False

        return True
