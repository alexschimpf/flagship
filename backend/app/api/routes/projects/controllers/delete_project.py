from app.api.schemas import SuccessResponse
from app.services.database.mysql.schemas.project import ProjectsTable
from app.services.database.mysql.service import MySQLService


class DeleteProjectController:

    def __init__(self, project_id: int):
        self.project_id = project_id

    def handle_request(self) -> SuccessResponse:
        self._delete_project()
        return SuccessResponse()

    def _delete_project(self) -> None:
        with MySQLService.get_session() as session:
            ProjectsTable.delete_project(project_id=self.project_id, session=session)
            session.commit()
