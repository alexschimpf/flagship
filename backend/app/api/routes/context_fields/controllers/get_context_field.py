from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.context_fields.schemas import ContextField
from app.services.database.mysql.schemas.context_field import ContextFieldRow
from app.services.database.mysql.service import MySQLService


class GetContextFieldController:

    def __init__(self, project_id: int, context_field_id: int):
        self.project_id = project_id
        self.context_field_id = context_field_id

    def handle_request(self) -> ContextField:
        with MySQLService.get_session() as session:
            context_field_row = session.get(ContextFieldRow, (self.context_field_id, self.project_id))

        if not context_field_row:
            raise NotFoundException

        return ContextField.from_row(row=context_field_row)
