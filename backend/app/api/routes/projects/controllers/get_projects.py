from app.api.routes.projects.schemas import Projects, Project
from app.services.database.mysql.schemas.project import ProjectsTable
from app.services.database.mysql.service import MySQLService


class GetProjectsController:

    def __init__(self) -> None:
        pass

    @staticmethod
    def handle_request() -> Projects:
        # TODO: Only return projects allowed for user
        with MySQLService.get_session() as session:
            project_rows = ProjectsTable.get_projects(session=session)

        projects = [
            Project.from_row(row=project_row)
            for project_row in project_rows
        ]

        return Projects(
            items=projects
        )
