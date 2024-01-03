from app.api.routes.projects.schemas import Projects, Project
from app.api.schemas import User
from app.services.database.mysql.schemas.project import ProjectsTable
from app.services.database.mysql.service import MySQLService


class GetProjectsController:

    def __init__(self, me: User) -> None:
        self.me = me

    def handle_request(self) -> Projects:
        with MySQLService.get_session() as session:
            project_rows = ProjectsTable.get_projects(session=session)

        projects = [
            Project.from_row(row=project_row)
            for project_row in project_rows
            if project_row.project_id in self.me.projects
        ]

        return Projects(
            items=projects
        )
