from sqlalchemy import Integer, select, delete, insert, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Session

from app.services.database.mysql.schemas.base import BaseRow


class UserProjectRow(BaseRow):

    __tablename__ = 'users_projects'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.project_id'), primary_key=True)


class UsersProjectsTable:

    @staticmethod
    def get_user_projects(user_id: int, session: Session) -> list[int]:
        return list(session.scalars(
            select(
                UserProjectRow.project_id
            ).where(
                UserProjectRow.user_id == user_id
            )
        ))

    @staticmethod
    def update_user_projects(user_id: int, project_ids: list[int], session: Session) -> None:
        session.execute(
            delete(
                UserProjectRow
            ).where(
                UserProjectRow.user_id == user_id
            )
        )

        session.execute(
            insert(
                UserProjectRow
            ),
            [
                {
                    'user_id': user_id,
                    'project_id': project_id
                } for project_id in project_ids
            ]
        )
