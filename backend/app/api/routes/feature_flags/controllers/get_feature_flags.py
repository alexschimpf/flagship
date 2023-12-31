from app.api.routes.feature_flags.schemas import FeatureFlags, FeatureFlag
from app.services.database.mysql.service import MySQLService
from app.services.database.mysql.models.feature_flag import FeatureFlagModel


class GetFeatureFlagsController:

    def __init__(self, project_id: int):
        self.project_id = project_id

    def handle_request(self):
        with MySQLService.get_session() as session:
            feature_flag_models = FeatureFlagModel.get_feature_flags(project_id=self.project_id, session=session)

        feature_flags = [
            FeatureFlag.from_model(model=feature_flag_model)
            for feature_flag_model in feature_flag_models
        ]

        return FeatureFlags(
            items=feature_flags
        )
