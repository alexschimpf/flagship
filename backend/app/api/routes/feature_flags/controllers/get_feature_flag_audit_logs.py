from app.api.exceptions.exceptions import UnauthorizedException
from app.api.routes.feature_flags.schemas import FeatureFlagAuditLogs, FeatureFlagAuditLog, FeatureFlagChange
from app.api.schemas import User
from app.constants import Permission
from app.services.database.mysql.schemas.feature_flag_audit_logs import FeatureFlagAuditLogsTable, \
    FeatureFlagAuditLogRow


class GetFeatureFlagAuditLogsController:

    def __init__(self, project_id: int, feature_flag_id: int, me: User):
        self.project_id = project_id
        self.feature_flag_id = feature_flag_id
        self.me = me

    def handle_request(self) -> FeatureFlagAuditLogs:
        if not self.me.role.has_permission(Permission.READ_FEATURE_FLAG_AUDIT_LOGS):
            raise UnauthorizedException

        audit_logs = FeatureFlagAuditLogsTable.get_feature_flag_audit_logs(
            project_id=self.project_id, feature_flag_id=self.feature_flag_id
        )

        result = []
        for i, audit_log in enumerate(audit_logs):
            prev = audit_logs[i-1] if i > 0 else None
            changes = self._get_changes(old=prev, new_=audit_log)
            if changes:
                result.append(FeatureFlagAuditLog(
                    actor=audit_log.actor,
                    event_time=audit_log.created_date,
                    changes=changes
                ))

        result.reverse()
        return FeatureFlagAuditLogs(items=result)

    @staticmethod
    def _get_changes(
        old: FeatureFlagAuditLogRow | None,
        new_: FeatureFlagAuditLogRow
    ) -> list[FeatureFlagChange]:
        changes: list[FeatureFlagChange] = []
        for field, display_name in (
            ('name', 'Name'),
            ('description', 'Description'),
            ('conditions', 'Conditions'),
            ('enabled', 'Enabled'),
        ):
            old_val = getattr(old, field) if old else None
            new_val = getattr(new_, field)
            if not old or old_val != new_val:
                if field == 'enabled':
                    if old:
                        old_val = str(old_val).lower()
                    new_val = str(new_val).lower()

                changes.append(FeatureFlagChange(
                    field=display_name,
                    old=old_val,
                    new=new_val
                ))

        return changes
