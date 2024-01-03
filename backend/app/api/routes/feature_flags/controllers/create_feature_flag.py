from typing import Any

import ujson

from app.api.exceptions.exceptions import NameTakenException, AppException, AggregateException, UnauthorizedException
from app.api.routes.feature_flags.controllers import common
from app.api.routes.feature_flags.schemas import CreateOrUpdateFeatureFlag, FeatureFlag
from app.api.schemas import User
from app.constants import Permission
from app.services.database.mysql.schemas.feature_flag import FeatureFlagRow, FeatureFlagsTable
from app.services.database.mysql.service import MySQLService


class CreateFeatureFlagController:

    def __init__(self, project_id: int, request: CreateOrUpdateFeatureFlag, me: User):
        self.project_id = project_id
        self.request = request
        self.me = me

    def handle_request(self) -> FeatureFlag:
        self._validate()

        feature_flag_row = self._create_feature_flag()

        return FeatureFlag.from_row(row=feature_flag_row)

    def _validate(self) -> None:
        if not self.me.role.has_permission(Permission.CREATE_FEATURE_FLAG):
            raise UnauthorizedException

        errors: list[AppException] = []
        with MySQLService.get_session() as session:
            if FeatureFlagsTable.is_feature_flag_name_taken(
                name=self.request.name,
                project_id=self.project_id,
                session=session
            ):
                errors.append(NameTakenException(field='name'))

            try:
                common.validate_feature_flag_conditions(
                    project_id=self.project_id, conditions=self.request.conditions, session=session)
            except AppException as e:
                errors.append(e)

        if errors:
            raise AggregateException(exceptions=errors)

    def _create_feature_flag(self) -> FeatureFlagRow:
        conditions: list[list[dict[str, Any]]] = []
        for and_group in self.request.conditions:
            conditions.append([
                condition.model_dump() for condition in and_group
            ])

        with MySQLService.get_session() as session:
            feature_flag_row = FeatureFlagRow(
                project_id=self.project_id,
                name=self.request.name,
                description=self.request.description,
                conditions=ujson.dumps(conditions),
                enabled=self.request.enabled
            )
            session.add(feature_flag_row)
            session.commit()
            session.refresh(feature_flag_row)

        return feature_flag_row
