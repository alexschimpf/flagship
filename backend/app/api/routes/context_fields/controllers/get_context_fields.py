from app.api.routes.context_fields.schemas import ContextFields, ContextField
from app.services.database.mysql.schemas.context_field import ContextFieldsTable
from app.services.database.mysql.service import MySQLService


class GetContextFieldsController:

    def __init__(self, project_id: int) -> None:
        self.project_id = project_id

    def handle_request(self) -> ContextFields:
        with MySQLService.get_session() as session:
            context_field_rows = ContextFieldsTable.get_context_fields(project_id=self.project_id, session=session)

        context_fields = [
            ContextField.from_row(row=context_field_row)
            for context_field_row in context_field_rows
        ]

        return ContextFields(
            items=context_fields
        )
