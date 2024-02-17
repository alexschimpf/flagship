from typing import cast

import ujson

from app.api.exceptions.exceptions import (
    NameTakenException,
    AggregateException,
    AppException,
    NotFoundException,
    UnauthorizedException,
    EnumContextFieldTypeWithoutEnumDefException,
    IllegalContextFieldEnumChangeException,
)
from app.api.routes.context_fields.controllers import common
from app.api.routes.context_fields.schemas import UpdateContextField, ContextField
from app.api.schemas import User
from app.constants import Permission, ContextValueType
from app.services.database.mysql.schemas.context_field import ContextFieldRow, ContextFieldsTable
from app.services.database.mysql.schemas.context_field_audit_logs import ContextFieldAuditLogRow
from app.services.database.mysql.service import MySQLService
from app.services.database.redis.service import RedisService


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
        if not self.me.role.has_permission(Permission.UPDATE_CONTEXT_FIELD) or self.project_id not in self.me.projects:
            raise UnauthorizedException

        errors: list[AppException] = []
        with MySQLService.get_session() as session:
            context_field_row = session.get(ContextFieldRow, self.context_field_id)
            if not context_field_row:
                raise NotFoundException

            self._validate_enum_def(context_field_row=context_field_row)

            if ContextFieldsTable.is_context_field_name_taken(
                name=self.request.name,
                project_id=self.project_id,
                context_field_id=self.context_field_id,
                session=session,
            ):
                errors.append(NameTakenException(field='name'))

        value_type = context_field_row.value_type
        enum_value_types = {ContextValueType.ENUM, ContextValueType.ENUM_LIST}
        if value_type in enum_value_types and not self.request.enum_def:
            errors.append(EnumContextFieldTypeWithoutEnumDefException(field='enum_def'))
        if value_type not in enum_value_types and self.request.enum_def:
            self.request.enum_def = None

        try:
            common.validate_enum_def(enum_def=self.request.enum_def)
        except AppException as e:
            errors.append(e)

        if errors:
            raise AggregateException(exceptions=errors)

    def _validate_enum_def(self, context_field_row: ContextFieldRow) -> None:
        # Don't allow enum def keys to be removed
        if context_field_row.enum_def_dict:
            existing_keys = set(context_field_row.enum_def_dict.keys())
            new_keys = set(self.request.enum_def.keys()) if self.request.enum_def else set()
            if existing_keys.difference(new_keys):
                raise IllegalContextFieldEnumChangeException

    def _update_context_field(self) -> ContextFieldRow:
        enum_def = ujson.dumps(self.request.enum_def) if self.request.enum_def else None
        with MySQLService.get_session() as session:
            ContextFieldsTable.update_context_field(
                project_id=self.project_id,
                context_field_id=self.context_field_id,
                name=self.request.name,
                enum_def=enum_def,
                description=self.request.description,
                session=session,
            )
            session.add(
                ContextFieldAuditLogRow(
                    context_field_id=self.context_field_id,
                    project_id=self.project_id,
                    actor=self.me.email,
                    name=self.request.name,
                    description=self.request.description,
                    enum_def=enum_def,
                )
            )
            session.commit()

            context_field_row = session.get(ContextFieldRow, self.context_field_id)

        if context_field_row:
            RedisService.add_or_replace_context_field(
                project_id=self.project_id,
                context_field_key=context_field_row.field_key,
                context_value_type=ContextValueType(context_field_row.value_type),
            )

        return cast(ContextFieldRow, context_field_row)
