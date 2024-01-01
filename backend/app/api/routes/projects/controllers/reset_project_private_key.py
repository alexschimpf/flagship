from typing import cast

from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.projects.controllers import common
from app.api.routes.projects.schemas import ProjectWithPrivateKey
from app.services.database.mysql.schemas.project import ProjectRow, ProjectsTable
from app.services.database.mysql.service import MySQLService


class ResetProjectPrivateKeyController:

    def __init__(self, project_id: int):
        self.project_id = project_id

    def handle_request(self) -> ProjectWithPrivateKey:
        self._validate()
        project_row, private_key = self._reset_private_key()

        return ProjectWithPrivateKey(
            project_id=project_row.project_id,
            name=project_row.name,
            private_key=private_key,
            created_date=project_row.created_date,
            updated_date=project_row.updated_date
        )

    def _validate(self) -> None:
        with MySQLService.get_session() as session:
            if not session.get(ProjectRow, self.project_id):
                raise NotFoundException

    def _reset_private_key(self) -> tuple[ProjectRow, str]:
        private_key, encrypted_private_key = common.generate_private_key()
        with MySQLService.get_session() as session:
            ProjectsTable.update_project_private_key(
                project_id=self.project_id, private_key=encrypted_private_key, session=session)
            session.commit()

            project_row = session.get(ProjectRow, self.project_id)

        return cast(ProjectRow, project_row), private_key
