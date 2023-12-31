import ujson

from app.api.exceptions.exceptions import NameTakenException
from app.api.routes.feature_flags.schemas import CreateOrUpdateFeatureFlag
from app.api.routes.feature_flags.schemas import FeatureFlag
from app.services.database.mysql.schemas.feature_flag import FeatureFlagRow, FeatureFlagsTable
from app.services.database.mysql.service import MySQLService


class CreateFeatureFlagController:

    def __init__(self, project_id: int, request: CreateOrUpdateFeatureFlag):
        self.project_id = project_id
        self.request = request

    def handle_request(self) -> FeatureFlag:
        self._validate()

        feature_flag_row = self._create_feature_flag()

        return FeatureFlag.from_row(row=feature_flag_row)

    def _validate(self) -> None:
        # TODO: Validate conditions

        with MySQLService.get_session() as session:
            if FeatureFlagsTable.is_feature_flag_name_taken(
                name=self.request.name,
                project_id=self.project_id,
                session=session
            ):
                raise NameTakenException(field='name')

    def _create_feature_flag(self) -> FeatureFlagRow:
        with MySQLService.get_session() as session:
            feature_flag_row = FeatureFlagRow(
                project_id=self.project_id,
                name=self.request.name,
                description=self.request.description,
                conditions=ujson.dumps(self.request.conditions),
                enabled=self.request.enabled
            )
            session.add(feature_flag_row)
            session.commit()
            session.refresh(feature_flag_row)

        return feature_flag_row
