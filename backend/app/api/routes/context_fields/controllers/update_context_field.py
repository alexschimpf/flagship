from typing import cast

import ujson

from app.api.exceptions.exceptions import NameTakenException, AggregateException, AppException, NotFoundException, \
    UnauthorizedException
from app.api.routes.context_fields.controllers import common
from app.api.routes.context_fields.schemas import UpdateContextField, ContextField
from app.api.schemas import User
from app.constants import Permission
from app.services.database.mysql.schemas.context_field import ContextFieldRow, ContextFieldsTable
from app.services.database.mysql.schemas.context_field_audit_logs import ContextFieldAuditLogRow
from app.services.database.mysql.service import MySQLService


class UpdateContextFieldController:

    def __init__(self, project_id: int, context_field_id: int, request: UpdateContextField, me: User):
        self.project_id = project_id
        self.context_field_id = context_field_id
        self.request = request
        self.me = me

    def handle_request(self) -> ContextField:
        self._validate()
        context_field_row = self._update_context_field()

        return ContextField.from_row(row=context_field_row)

    def _validate(self) -> None:
        if (not self.me.role.has_permission(Permission.UPDATE_CONTEXT_FIELD) or
                self.project_id not in self.me.projects):
            raise UnauthorizedException

        errors: list[AppException] = []
        with MySQLService.get_session() as session:
            if not session.get(ContextFieldRow, self.context_field_id):
                raise NotFoundException

            if ContextFieldsTable.is_context_field_name_taken(
                name=self.request.name,
                project_id=self.project_id,
                context_field_id=self.context_field_id,
                session=session
            ):
                errors.append(NameTakenException(field='name'))

        try:
            common.validate_enum_def(enum_def=self.request.enum_def)
        except AppException as e:
            errors.append(e)

        if errors:
            raise AggregateException(exceptions=errors)

    def _update_context_field(self) -> ContextFieldRow:
        enum_def = ujson.dumps(self.request.enum_def) if self.request.enum_def else None
        with MySQLService.get_session() as session:
            ContextFieldsTable.update_context_field(
                project_id=self.project_id,
                context_field_id=self.context_field_id,
                name=self.request.name,
                enum_def=enum_def,
                description=self.request.description,
                session=session
            )
            session.add(ContextFieldAuditLogRow(
                context_field_id=self.context_field_id,
                project_id=self.project_id,
                actor=self.me.email,
                name=self.request.name,
                description=self.request.description,
                enum_def=enum_def
            ))
            session.commit()

            context_field_row = session.get(ContextFieldRow, self.context_field_id)

        return cast(ContextFieldRow, context_field_row)
