import ujson

from app.api.exceptions.exceptions import NotFoundException, NameTakenException
from app.api.routes.feature_flags.schemas import CreateOrUpdateFeatureFlag, FeatureFlag
from app.services.database.mysql.schemas.feature_flag import FeatureFlagRow, FeatureFlagsTable
from app.services.database.mysql.service import MySQLService


class UpdateFeatureFlagController:

    def __init__(self, project_id: int, feature_flag_id: int, request: CreateOrUpdateFeatureFlag):
        self.project_id = project_id
        self.feature_flag_id = feature_flag_id
        self.request = request

    def handle_request(self) -> FeatureFlag:
        self._validate()

        feature_flag_row = self._update_feature_flag()

        if not feature_flag_row:
            raise NotFoundException

        return FeatureFlag.from_row(row=feature_flag_row)

    def _validate(self) -> None:
        # TODO: Validate conditions

        with MySQLService.get_session() as session:
            if FeatureFlagsTable.is_feature_flag_name_taken(
                name=self.request.name,
                feature_flag_id=self.feature_flag_id,
                project_id=self.project_id,
                session=session
            ):
                raise NameTakenException(field='name')

    def _update_feature_flag(self) -> FeatureFlagRow | None:
        with MySQLService.get_session() as session:
            FeatureFlagsTable.update_feature_flag(
                project_id=self.project_id,
                feature_flag_id=self.feature_flag_id,
                name=self.request.name,
                description=self.request.description,
                enabled=self.request.enabled,
                conditions=ujson.dumps(self.request.conditions),
                session=session
            )
            session.commit()

            feature_flag_row = session.get(FeatureFlagRow, (self.feature_flag_id, self.project_id))

        return feature_flag_row
