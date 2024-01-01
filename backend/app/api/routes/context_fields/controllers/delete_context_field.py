from app.api.schemas import SuccessResponse
from app.services.database.mysql.schemas.context_field import ContextFieldsTable, ContextFieldRow
from app.services.database.mysql.service import MySQLService
from app.api.exceptions.exceptions import NotFoundException


class DeleteContextFieldController:

    def __init__(self, project_id: int, context_field_id: int):
        self.project_id = project_id
        self.context_field_id = context_field_id

    def handle_request(self) -> SuccessResponse:
        self._validate()
        self._delete_context_field()

        return SuccessResponse()

    def _validate(self) -> None:
        with MySQLService.get_session() as session:
            if not session.get(ContextFieldRow, (self.context_field_id, self.project_id)):
                raise NotFoundException

    def _delete_context_field(self) -> None:
        with MySQLService.get_session() as session:
            ContextFieldsTable.delete_context_field(
                project_id=self.project_id,
                context_field_id=self.context_field_id,
                session=session
            )
            session.commit()
