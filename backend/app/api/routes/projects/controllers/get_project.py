from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.projects.schemas import Project
from app.services.database.mysql.models.project import ProjectModel
from app.services.database.mysql.service import MySQLService


class GetProjectController:

    def __init__(self, project_id: int):
        self.project_id = project_id

    def handle_request(self) -> Project:
        with MySQLService.get_session() as session:
            project_model = session.get(ProjectModel, self.project_id)

        if not project_model:
            raise NotFoundException

        return Project.from_model(model=project_model)
