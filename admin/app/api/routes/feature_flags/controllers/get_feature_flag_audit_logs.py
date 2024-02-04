import ujson
from typing import Any

from app.api.exceptions.exceptions import UnauthorizedException
from app.api.routes.feature_flags.schemas import FeatureFlagAuditLogs, FeatureFlagAuditLog, FeatureFlagChange, \
    FeatureFlagCondition
from app.api.schemas import User
from app.constants import Permission, OPERATOR_DISPLAY_NAMES
from app.services.database.mysql.schemas.feature_flag_audit_logs import FeatureFlagAuditLogsTable, \
    FeatureFlagAuditLogRow
from app.services.database.mysql.service import MySQLService


class GetFeatureFlagAuditLogsController:

    def __init__(self, project_id: int, feature_flag_id: int, page: int, page_size: int, me: User):
        self.project_id = project_id
        self.feature_flag_id = feature_flag_id
        self.page = page
        self.page_size = page_size
        self.me = me

    def handle_request(self) -> FeatureFlagAuditLogs:
        with MySQLService.get_session() as session:
            audit_logs, total_count = FeatureFlagAuditLogsTable.get_feature_flag_audit_logs(
                project_id=self.project_id, feature_flag_id=self.feature_flag_id,
                page=self.page, page_size=self.page_size, session=session
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
        return FeatureFlagAuditLogs(items=result, total=total_count)

    @classmethod
    def _get_changes(
        cls,
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

                if field == 'conditions':
                    old_val = cls._humanize_conditions(conditions=old_val)
                    new_val = cls._humanize_conditions(conditions=new_val)

                changes.append(FeatureFlagChange(
                    field=display_name,
                    old=old_val,
                    new=new_val
                ))

        return changes

    @classmethod
    def _humanize_conditions(cls, conditions: str) -> str:
        if not conditions:
            return conditions

        human_friendly_conditions: list[list[str]] = []
        conditions_list = ujson.loads(conditions)
        for condition_group in conditions_list:
            human_friendly_group: list[str] = []
            for condition in condition_group:
                human_friendly_condition = cls._humanize_condition(
                    condition=FeatureFlagCondition(**condition))
                human_friendly_group.append(human_friendly_condition)
            human_friendly_conditions.append(human_friendly_group)

        result: list[str] = []
        for group in human_friendly_conditions:
            result.append(f'({" OR ".join(group)})')

        if len(result) == 1:
            result[0] = result[0][1:-1]

        return ' AND '.join(result)

    @classmethod
    def _humanize_condition(cls, condition: FeatureFlagCondition) -> str:
        # TODO: Handle showing enum names instead of values
        operator_name = OPERATOR_DISPLAY_NAMES[condition.operator]
        value: Any = condition.value
        if isinstance(condition.value, list):
            value = ', '.join((
                cls._humanize_condition_value(value=x)
                for x in value
            ))
            value = f'[{value}]'
        else:
            value = cls._humanize_condition_value(value=value)
        return f'`{condition.context_key}` {operator_name} {value}'

    @staticmethod
    def _humanize_condition_value(value: Any) -> str:
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        else:
            return str(value)
