from typing import cast, Any

import ujson

from app.api.exceptions.exceptions import (
    NotFoundException,
    NameTakenException,
    AppException,
    AggregateException,
    UnauthorizedException,
)
from app.api.routes.feature_flags.controllers import common
from app.api.routes.feature_flags.schemas import CreateOrUpdateFeatureFlag, FeatureFlag
from app.api.schemas import User
from app.constants import Permission
from app.services.database.mysql.schemas.feature_flag import FeatureFlagRow, FeatureFlagsTable
from app.services.database.mysql.schemas.feature_flag_audit_logs import FeatureFlagAuditLogRow
from app.services.database.mysql.service import MySQLService
from app.services.database.redis.service import RedisService


class UpdateFeatureFlagController:
    def __init__(self, project_id: int, feature_flag_id: int, request: CreateOrUpdateFeatureFlag, me: User):
        self.project_id = project_id
        self.feature_flag_id = feature_flag_id
        self.request = request
        self.me = me

    def handle_request(self) -> FeatureFlag:
        self._validate()
        feature_flag_row = self._update_feature_flag()

        return FeatureFlag.from_row(row=feature_flag_row)

    def _validate(self) -> None:
        if not self.me.role.has_permission(Permission.UPDATE_FEATURE_FLAG) or self.project_id not in self.me.projects:
            raise UnauthorizedException

        errors: list[AppException] = []
        with MySQLService.get_session() as session:
            if not session.get(FeatureFlagRow, self.feature_flag_id):
                raise NotFoundException

            if FeatureFlagsTable.is_feature_flag_name_taken(
                name=self.request.name,
                feature_flag_id=self.feature_flag_id,
                project_id=self.project_id,
                session=session,
            ):
                errors.append(NameTakenException(field='name'))

            try:
                common.validate_feature_flag_conditions(
                    project_id=self.project_id, conditions=self.request.conditions, session=session
                )
            except AppException as e:
                errors.append(e)

        if errors:
            raise AggregateException(exceptions=errors)

    def _update_feature_flag(self) -> FeatureFlagRow:
        conditions: list[list[dict[str, Any]]] = []
        for and_group in self.request.conditions:
            conditions.append([condition.model_dump() for condition in and_group])

        with MySQLService.get_session() as session:
            FeatureFlagsTable.update_feature_flag(
                project_id=self.project_id,
                feature_flag_id=self.feature_flag_id,
                name=self.request.name,
                description=self.request.description,
                enabled=self.request.enabled,
                conditions=ujson.dumps(conditions),
                session=session,
            )
            audit_log_row = FeatureFlagAuditLogRow(
                feature_flag_id=self.feature_flag_id,
                project_id=self.project_id,
                actor=self.me.email,
                name=self.request.name,
                description=self.request.description,
                conditions=ujson.dumps(conditions),
                enabled=self.request.enabled,
            )
            session.add(audit_log_row)
            session.commit()

            feature_flag_row = session.get(FeatureFlagRow, self.feature_flag_id)

        RedisService.add_or_replace_feature_flag(
            project_id=self.project_id,
            feature_flag_name=self.request.name,
            conditions=self.request.conditions,
            is_enabled=self.request.enabled,
        )

        return cast(FeatureFlagRow, feature_flag_row)
