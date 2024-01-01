from app.api.exceptions.exceptions import NotFoundException
from app.api.schemas import SuccessResponse
from app.services.database.mysql.schemas.project import ProjectsTable, ProjectRow
from app.services.database.mysql.service import MySQLService


class DeleteProjectController:

    def __init__(self, project_id: int):
        self.project_id = project_id

    def handle_request(self) -> SuccessResponse:
        self._validate()
        self._delete_project()
        return SuccessResponse()

    def _validate(self) -> None:
        with MySQLService.get_session() as session:
            if not session.get(ProjectRow, self.project_id):
                raise NotFoundException

    def _delete_project(self) -> None:
        with MySQLService.get_session() as session:
            ProjectsTable.delete_project(project_id=self.project_id, session=session)
            session.commit()
