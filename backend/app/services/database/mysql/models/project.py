from typing import Self
import datetime
from sqlalchemy.sql import func, text
from sqlalchemy import String, DateTime, Integer, delete, Sequence, select, update
from sqlalchemy.orm import Mapped, mapped_column, Session

from app.services.database.mysql.models.base import BaseModel


class ProjectModel(BaseModel):

    __tablename__ = 'projects'

    project_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    private_key: Mapped[str] = mapped_column(String(184))
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.current_timestamp())
    updated_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    @classmethod
    def get_project_by_name(cls, name: str, session: Session) -> Self:
        return session.scalar(
            select(
                ProjectModel
            ).where(
                ProjectModel.name == name
            )
        )

    @classmethod
    def get_projects(cls, session: Session) -> Sequence[Self]:
        return session.scalars(
            select(
                ProjectModel
            )
        ).all()

    @staticmethod
    def delete_project(project_id: int, session: Session) -> None:
        session.execute(
            delete(
                ProjectModel
            ).where(
                ProjectModel.project_id == project_id
            )
        )

    @staticmethod
    def update_project(project_id: int, name: str, session: Session) -> None:
        session.execute(
            update(
                ProjectModel
            ).where(
                ProjectModel.project_id == project_id
            ).values({
                ProjectModel.name: name
            })
        )

    @staticmethod
    def update_project_private_key(project_id: int, private_key: str, session: Session) -> None:
        session.execute(
            update(
                ProjectModel
            ).where(
                ProjectModel.project_id == project_id
            ).values({
                ProjectModel.private_key: private_key
            })
        )
