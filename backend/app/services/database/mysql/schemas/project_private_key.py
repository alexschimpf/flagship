from sqlalchemy import String, Integer, ForeignKey, delete
from sqlalchemy.orm import Mapped, mapped_column, Session

from app.services.database.mysql.schemas.base import BaseRow


class ProjectPrivateKeyRow(BaseRow):

    __tablename__ = 'project_private_keys'

    project_private_key_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.project_id'))
    private_key: Mapped[str] = mapped_column(String(184))


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
