import ujson

from app.api.exceptions.exceptions import NameTakenException, ContextFieldKeyTakenException, AggregateException, \
    AppException
from app.api.routes.context_fields.schemas import CreateContextField, ContextField
from app.services.database.mysql.schemas.context_field import ContextFieldRow, ContextFieldsTable
from app.services.database.mysql.service import MySQLService


class CreateContextFieldController:

    def __init__(self, project_id: int, request: CreateContextField):
        self.project_id = project_id
        self.request = request

    def handle_request(self) -> ContextField:
        self._validate()

        context_field_row = self._create_context_field()

        return ContextField.from_row(row=context_field_row)

    def _validate(self) -> None:
        errors: list[AppException] = []

        with MySQLService.get_session() as session:
            if ContextFieldsTable.is_context_field_name_taken(
                name=self.request.name,
                project_id=self.project_id,
                session=session
            ):
                errors.append(NameTakenException(field='name'))

            if ContextFieldsTable.is_context_field_field_key_taken(
                field_key=self.request.field_key,
                project_id=self.project_id,
                session=session
            ):
                errors.append(ContextFieldKeyTakenException(field='field_key'))

        if errors:
            raise AggregateException(exceptions=errors)

    def _create_context_field(self) -> ContextFieldRow:
        enum_def = ujson.dumps(self.request.enum_def) if self.request.enum_def else None
        with MySQLService.get_session() as session:
            context_field_row = ContextFieldRow(
                project_id=self.project_id,
                name=self.request.name,
                description=self.request.description,
                field_key=self.request.field_key,
                value_type=self.request.value_type.value,
                enum_def=enum_def
            )
            session.add(context_field_row)
            session.commit()
            session.refresh(context_field_row)

        return context_field_row
