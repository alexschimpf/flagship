from app.api.routes.context_fields.schemas import ContextFields, ContextField
from app.services.database.mysql.schemas.context_field import ContextFieldsTable
from app.services.database.mysql.service import MySQLService


class GetContextFieldsController:

    def __init__(self, project_id: int, page: int, page_size: int) -> None:
        self.project_id = project_id
        self.page = page
        self.page_size = page_size

    def handle_request(self) -> ContextFields:
        with MySQLService.get_session() as session:
            context_field_rows, total_count = ContextFieldsTable.get_context_fields(
                project_id=self.project_id, page=self.page, page_size=self.page_size, session=session)

        context_fields = [
            ContextField.from_row(row=context_field_row)
            for context_field_row in context_field_rows
        ]

        return ContextFields(
            items=context_fields,
            total=total_count
        )
