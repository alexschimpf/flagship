from app.api.exceptions.exceptions import NotFoundException, UnauthorizedException
from app.api.routes.projects.schemas import Project
from app.api.schemas import User
from app.services.database.mysql.schemas.project import ProjectRow
from app.services.database.mysql.service import MySQLService


class GetProjectController:
    def __init__(self, project_id: int, me: User):
        self.project_id = project_id
        self.me = me

    def handle_request(self) -> Project:
        if self.project_id not in self.me.projects:
            raise UnauthorizedException

        with MySQLService.get_session() as session:
            project_row = session.get(ProjectRow, self.project_id)

        if not project_row:
            raise NotFoundException

        return Project.from_row(row=project_row)
