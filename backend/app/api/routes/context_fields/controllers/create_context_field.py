import ujson

from app.api.exceptions.exceptions import NameTakenException, ContextFieldKeyTakenException, AggregateException, \
    AppException, EnumContextFieldTypeWithoutEnumDefException, UnauthorizedException
from app.api.routes.context_fields.controllers import common
from app.api.routes.context_fields.schemas import CreateContextField, ContextField
from app.api.schemas import User
from app.constants import ContextValueType, Permission, AuditLogEventType
from app.services.database.mysql.schemas.context_field import ContextFieldRow, ContextFieldsTable
from app.services.database.mysql.schemas.context_field_audit_logs import ContextFieldAuditLogRow
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogRow
from app.services.database.mysql.service import MySQLService


class CreateContextFieldController:

    def __init__(self, project_id: int, request: CreateContextField, me: User):
        self.project_id = project_id
        self.request = request
        self.me = me

    def handle_request(self) -> ContextField:
        self._validate()
        context_field_row = self._create_context_field()

        return ContextField.from_row(row=context_field_row)

    def _validate(self) -> None:
        if (not self.me.role.has_permission(Permission.CREATE_CONTEXT_FIELD) or
                self.project_id not in self.me.projects):
            raise UnauthorizedException

        errors: list[AppException] = []

        self._validate_enum_def_and_type(errors=errors)

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

    def _validate_enum_def_and_type(self, errors: list[AppException]) -> None:
        enum_value_types = {ContextValueType.ENUM, ContextValueType.ENUM_LIST}

        if self.request.value_type in enum_value_types and not self.request.enum_def:
            errors.append(EnumContextFieldTypeWithoutEnumDefException(field='enum_def'))

        if self.request.value_type not in enum_value_types and self.request.enum_def:
            # Clear this field, since it isn't applicable for non-enum types
            self.request.enum_def = None

        try:
            common.validate_enum_def(enum_def=self.request.enum_def)
        except AppException as e:
            errors.append(e)

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
            session.flush()

            session.add(ContextFieldAuditLogRow(
                context_field_id=context_field_row.context_field_id,
                project_id=self.project_id,
                actor=self.me.email,
                name=context_field_row.name,
                description=context_field_row.description,
                enum_def=context_field_row.enum_def
            ))

            session.add(SystemAuditLogRow(
                actor=self.me.email,
                event_type=AuditLogEventType.CREATED_CONTEXT_FIELD,
                details=f'Name: {context_field_row.name}'
            ))

            session.commit()
            session.refresh(context_field_row)

        return context_field_row
