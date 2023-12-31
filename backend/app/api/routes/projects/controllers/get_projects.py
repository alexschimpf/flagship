from app.api.routes.projects.schemas import Projects, Project
from app.services.database.mysql.service import MySQLService
from app.services.database.mysql.models.project import ProjectModel


class GetProjectsController:

    def __init__(self) -> None:
        pass

    @staticmethod
    def handle_request() -> Projects:
        # TODO: Only return projects allowed for user
        with MySQLService.get_session() as session:
            project_models = ProjectModel.get_projects(session=session)

        projects = [
            Project.from_model(model=project_model)
            for project_model in project_models
        ]

        return Projects(
            items=projects
        )
