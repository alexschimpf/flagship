from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.projects.schemas import CreateOrUpdateProject, Project
from app.services.database.mysql.models.project import ProjectModel
from app.services.database.mysql.service import MySQLService


class UpdateProjectController:

    def __init__(self, project_id: int, request: CreateOrUpdateProject):
        self.project_id = project_id
        self.request = request

    def handle_request(self) -> Project:
        project_model = self._update_project()
        if not project_model:
            raise NotFoundException

        return Project.from_model(model=project_model)

    def _update_project(self) -> ProjectModel | None:
        with MySQLService.get_session() as session:
            ProjectModel.update_project(project_id=self.project_id, name=self.request.name, session=session)
            session.commit()

            project_model = session.get(ProjectModel, self.project_id)

        return project_model
