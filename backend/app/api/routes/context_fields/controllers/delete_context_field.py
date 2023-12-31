from app.api.schemas import SuccessResponse
from app.services.database.mysql.schemas.context_field import ContextFieldsTable
from app.services.database.mysql.service import MySQLService


class DeleteContextFieldController:

    def __init__(self, project_id: int, context_field_id: int):
        self.project_id = project_id
        self.context_field_id = context_field_id

    def handle_request(self) -> SuccessResponse:
        with MySQLService.get_session() as session:
            ContextFieldsTable.delete_context_field(
                project_id=self.project_id,
                context_field_id=self.context_field_id,
                session=session
            )
            session.commit()

        return SuccessResponse()
