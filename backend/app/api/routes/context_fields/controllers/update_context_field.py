import ujson

from app.api.routes.context_fields.schemas import UpdateContextField, ContextField
from app.services.database.mysql.models.context_field import ContextFieldModel
from app.services.database.mysql.service import MySQLService
from app.api.exceptions.exceptions import NameTakenException, AggregateException, AppException, NotFoundException


class UpdateContextFieldController:

    def __init__(self, project_id: int, context_field_id: int, request: UpdateContextField):
        self.project_id = project_id
        self.context_field_id = context_field_id
        self.request = request

    def handle_request(self) -> ContextField:
        self._validate()

        context_field_model = self._update_context_field()
        if not context_field_model:
            raise NotFoundException

        return ContextField.from_model(model=context_field_model)

    def _validate(self) -> None:
        errors: list[AppException] = []

        with MySQLService.get_session() as session:
            if ContextFieldModel.is_context_field_name_taken(
                name=self.request.name,
                project_id=self.project_id,
                context_field_id=self.context_field_id,
                session=session
            ):
                errors.append(NameTakenException(field='name'))

        if errors:
            raise AggregateException(exceptions=errors)

    def _update_context_field(self) -> ContextFieldModel | None:
        enum_def = ujson.dumps(self.request.enum_def) if self.request.enum_def else None
        with MySQLService.get_session() as session:
            ContextFieldModel.update_context_field(
                project_id=self.project_id,
                context_field_id=self.context_field_id,
                name=self.request.name,
                enum_def=enum_def,
                description=self.request.description,
                session=session
            )
            session.commit()

            context_field_model = session.get(ContextFieldModel, (self.context_field_id, self.project_id))

        return context_field_model
