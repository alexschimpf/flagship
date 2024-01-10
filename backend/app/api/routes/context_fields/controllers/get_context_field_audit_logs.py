from app.api.exceptions.exceptions import UnauthorizedException
from app.api.routes.context_fields.schemas import ContextFieldAuditLogs, ContextFieldAuditLog, ContextFieldChange
from app.api.schemas import User
from app.constants import Permission
from app.services.database.mysql.schemas.context_field_audit_logs import ContextFieldAuditLogRow, \
    ContextFieldAuditLogsTable


class GetContextFieldAuditLogsController:

    def __init__(self, project_id: int, context_field_id: int, page: int, page_size: int, me: User):
        self.project_id = project_id
        self.context_field_id = context_field_id
        self.page = page
        self.page_size = page_size
        self.me = me

    def handle_request(self) -> ContextFieldAuditLogs:
        if not self.me.role.has_permission(Permission.READ_CONTEXT_FIELD_AUDIT_LOGS):
            raise UnauthorizedException

        audit_logs, total_count = ContextFieldAuditLogsTable.get_context_field_audit_logs(
            project_id=self.project_id, context_field_id=self.context_field_id,
            page=self.page, page_size=self.page_size
        )

        result = []
        for i, audit_log in enumerate(audit_logs):
            prev = audit_logs[i-1] if i > 0 else None
            changes = self._get_changes(old=prev, new_=audit_log)
            if changes:
                result.append(ContextFieldAuditLog(
                    actor=audit_log.actor,
                    event_time=audit_log.created_date,
                    changes=changes
                ))

        result.reverse()
        return ContextFieldAuditLogs(items=result, total=total_count)

    @staticmethod
    def _get_changes(
        old: ContextFieldAuditLogRow | None,
        new_: ContextFieldAuditLogRow
    ) -> list[ContextFieldChange]:
        changes: list[ContextFieldChange] = []
        for field, display_name in (
            ('name', 'Name'),
            ('description', 'Description'),
            ('enum_def', 'Enum Definition')
        ):
            old_val = getattr(old, field) if old else None
            new_val = getattr(new_, field)
            if not old or old_val != new_val:
                changes.append(ContextFieldChange(
                    field=display_name,
                    old=old_val,
                    new=new_val
                ))

        return changes
