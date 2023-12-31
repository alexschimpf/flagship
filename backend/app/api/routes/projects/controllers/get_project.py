from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.projects.schemas import Project
from app.services.database.mysql.schemas.project import ProjectRow
from app.services.database.mysql.service import MySQLService


class GetProjectController:

    def __init__(self, project_id: int):
        self.project_id = project_id

    def handle_request(self) -> Project:
        with MySQLService.get_session() as session:
            project_row = session.get(ProjectRow, self.project_id)

        if not project_row:
            raise NotFoundException

        return Project.from_row(row=project_row)
