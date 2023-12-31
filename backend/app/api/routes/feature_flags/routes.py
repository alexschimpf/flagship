from fastapi import APIRouter

from app.api.routes.feature_flags.controllers.get_feature_flag import GetFeatureFlagController
from app.api.routes.feature_flags.controllers.get_feature_flags import GetFeatureFlagsController
from app.api.routes.feature_flags.controllers.create_feature_flag import CreateFeatureFlagController
from app.api.routes.feature_flags.controllers.delete_feature_flag import DeleteFeatureFlagController
from app.api.routes.feature_flags.controllers.update_feature_flag import UpdateFeatureFlagController
from app.api.routes.feature_flags.schemas import CreateOrUpdateFeatureFlag, FeatureFlag, FeatureFlags
from app.api.schemas import SuccessResponse

router = APIRouter(
    prefix='/feature_flags',
    tags=['Feature Flags']
)


@router.get('', response_model=FeatureFlags)
def get_feature_flags(project_id: int) -> FeatureFlags:
    return GetFeatureFlagsController(
        project_id=project_id
    ).handle_request()


@router.post('', response_model=FeatureFlag)
def create_feature_flag(project_id: int, request: CreateOrUpdateFeatureFlag) -> FeatureFlag:
    return CreateFeatureFlagController(
        project_id=project_id,
        request=request
    ).handle_request()


@router.get('/{feature_flag_id}', response_model=FeatureFlag)
def get_feature_flag(project_id: int, feature_flag_id: int) -> FeatureFlag:
    return GetFeatureFlagController(
        project_id=project_id,
        feature_flag_id=feature_flag_id
    ).handle_request()


@router.put('/{feature_flag_id}', response_model=FeatureFlag)
def update_feature_flag(project_id: int, feature_flag_id: int, request: CreateOrUpdateFeatureFlag) -> FeatureFlag:
    return UpdateFeatureFlagController(
        project_id=project_id,
        feature_flag_id=feature_flag_id,
        request=request
    ).handle_request()


@router.delete('/{feature_flag_id}', response_model=SuccessResponse)
def delete_feature_flag(project_id: int, feature_flag_id: int) -> SuccessResponse:
    return DeleteFeatureFlagController(
        project_id=project_id,
        feature_flag_id=feature_flag_id
    ).handle_request()
