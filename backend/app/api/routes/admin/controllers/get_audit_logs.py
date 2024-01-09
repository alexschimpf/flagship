from app.api.exceptions.exceptions import UnauthorizedException
from app.api.routes.admin.schemas import SystemAuditLog
from app.api.routes.admin.schemas import SystemAuditLogs
from app.api.schemas import User
from app.constants import Permission, AuditLogEventType
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogsTable


class GetAuditLogsController:

    def __init__(self, me: User):
        self.me = me

    def handle_request(self) -> SystemAuditLogs:
        if not self.me.role.has_permission(Permission.READ_SYSTEM_AUDIT_LOGS):
            raise UnauthorizedException

        result = []
        rows = SystemAuditLogsTable.get_system_audit_logs()
        for row in rows:
            event_type = ' '.join([
                word.capitalize() if i == 0 else word.lower()
                for i, word in enumerate(AuditLogEventType(row.event_type).name.split('_'))
            ])
            result.append(
                SystemAuditLog(
                    actor=row.actor,
                    event_time=row.created_date,
                    details=row.details,
                    event_type=event_type
                )
            )

        return SystemAuditLogs(items=result)
