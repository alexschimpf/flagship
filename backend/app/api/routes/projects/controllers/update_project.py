from typing import cast

from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.projects.schemas import CreateOrUpdateProject, Project
from app.services.database.mysql.schemas.project import ProjectRow, ProjectsTable
from app.services.database.mysql.service import MySQLService


class UpdateProjectController:

    def __init__(self, project_id: int, request: CreateOrUpdateProject):
        self.project_id = project_id
        self.request = request

    def handle_request(self) -> Project:
        self._validate()
        project_row = self._update_project()
        return Project.from_row(row=project_row)

    def _validate(self) -> None:
        with MySQLService.get_session() as session:
            if not session.get(ProjectRow, self.project_id):
                raise NotFoundException

    def _update_project(self) -> ProjectRow:
        with MySQLService.get_session() as session:
            ProjectsTable.update_project(project_id=self.project_id, name=self.request.name, session=session)
            session.commit()

            project_row = session.get(ProjectRow, self.project_id)

        return cast(ProjectRow, project_row)
