from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.context_fields.schemas import ContextField
from app.services.database.mysql.models.context_field import ContextFieldModel
from app.services.database.mysql.service import MySQLService


class GetContextFieldController:

    def __init__(self, project_id: int, context_field_id: int):
        self.project_id = project_id
        self.context_field_id = context_field_id

    def handle_request(self) -> ContextField:
        with MySQLService.get_session() as session:
            context_field_model = session.get(ContextFieldModel, (self.context_field_id, self.project_id))

        if not context_field_model:
            raise NotFoundException

        return ContextField.from_model(model=context_field_model)
