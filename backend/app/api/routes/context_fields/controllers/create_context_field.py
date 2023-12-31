import ujson

from app.api.routes.context_fields.schemas import CreateContextField, ContextField
from app.services.database.mysql.models.context_field import ContextFieldModel
from app.services.database.mysql.service import MySQLService
from app.api.exceptions.exceptions import NameTakenException, ContextFieldKeyTakenException, AggregateException, \
    AppException


class CreateContextFieldController:

    def __init__(self, project_id: int, request: CreateContextField):
        self.project_id = project_id
        self.request = request

    def handle_request(self) -> ContextField:
        self._validate()

        context_field_model = self._create_context_field()

        return ContextField.from_model(model=context_field_model)

    def _validate(self) -> None:
        errors: list[AppException] = []

        with MySQLService.get_session() as session:
            if ContextFieldModel.is_context_field_name_taken(
                name=self.request.name,
                project_id=self.project_id,
                session=session
            ):
                errors.append(NameTakenException(field='name'))

            if ContextFieldModel.is_context_field_field_key_taken(
                field_key=self.request.field_key,
                project_id=self.project_id,
                session=session
            ):
                errors.append(ContextFieldKeyTakenException(field='field_key'))

        if errors:
            raise AggregateException(exceptions=errors)

    def _create_context_field(self) -> ContextFieldModel:
        enum_def = ujson.dumps(self.request.enum_def) if self.request.enum_def else None
        with MySQLService.get_session() as session:
            context_field_model = ContextFieldModel(
                project_id=self.project_id,
                name=self.request.name,
                description=self.request.description,
                field_key=self.request.field_key,
                value_type=self.request.value_type.value,
                enum_def=enum_def
            )
            session.add(context_field_model)
            session.commit()
            session.refresh(context_field_model)

        return context_field_model
