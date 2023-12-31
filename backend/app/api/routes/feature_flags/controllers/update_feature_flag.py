import ujson

from app.services.database.mysql.service import MySQLService
from app.services.database.mysql.models.feature_flag import FeatureFlagModel
from app.api.routes.feature_flags.schemas import CreateOrUpdateFeatureFlag, FeatureFlag
from app.api.exceptions.exceptions import NotFoundException, NameTakenException


class UpdateFeatureFlagController:

    def __init__(self, project_id: int, feature_flag_id: int, request: CreateOrUpdateFeatureFlag):
        self.project_id = project_id
        self.feature_flag_id = feature_flag_id
        self.request = request

    def handle_request(self) -> FeatureFlag:
        self._validate()

        feature_flag_model = self._update_feature_flag()

        if not feature_flag_model:
            raise NotFoundException

        return FeatureFlag.from_model(model=feature_flag_model)

    def _validate(self):
        # TODO: Validate conditions

        with MySQLService.get_session() as session:
            if FeatureFlagModel.is_feature_flag_name_taken(
                name=self.request.name,
                feature_flag_id=self.feature_flag_id,
                project_id=self.project_id,
                session=session
            ):
                raise NameTakenException(field='name')

    def _update_feature_flag(self) -> FeatureFlagModel | None:
        with MySQLService.get_session() as session:
            FeatureFlagModel.update_feature_flag(
                project_id=self.project_id,
                feature_flag_id=self.feature_flag_id,
                name=self.request.name,
                description=self.request.description,
                enabled=self.request.enabled,
                conditions=ujson.dumps(self.request.conditions),
                session=session
            )
            session.commit()

            feature_flag_model = session.get(FeatureFlagModel, (self.feature_flag_id, self.project_id))

        return feature_flag_model
