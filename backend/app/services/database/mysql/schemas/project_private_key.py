from sqlalchemy import String, Integer, ForeignKey, delete, select, text
from sqlalchemy.orm import Mapped, mapped_column, Session

from app.services.database.mysql.schemas.base import BaseRow


class ProjectPrivateKeyRow(BaseRow):

    __tablename__ = 'project_private_keys'

    project_private_key_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.project_id'))
    private_key: Mapped[str] = mapped_column(String(184))
    name: Mapped[str] = mapped_column(String(128))


class ProjectPrivateKeysTable:

    @staticmethod
    def delete_project_private_key(project_id: int, project_private_key: int, session: Session) -> None:
        session.execute(
            delete(
                ProjectPrivateKeyRow
            ).where(
                ProjectPrivateKeyRow.project_id == project_id,
                ProjectPrivateKeyRow.project_private_key_id == project_private_key
            )
        )

    @staticmethod
    def is_project_private_key_name_taken(
        project_id: int,
        name: str,
        session: Session,
        project_private_key_id: int | None = None
    ) -> bool:
        where_conditions = [
            ProjectPrivateKeyRow.name == name,
            ProjectPrivateKeyRow.project_id == project_id
        ]
        if project_private_key_id is not None:
            where_conditions.append(
                ProjectPrivateKeyRow.project_private_key_id != project_private_key_id
            )

        return bool(session.scalar(
            select(
                text('1')
            ).select_from(
                ProjectPrivateKeyRow
            ).where(
                *where_conditions
            ).limit(1)
        ))
