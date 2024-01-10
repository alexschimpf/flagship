from fastapi import APIRouter, Depends

from app.api import auth
from app.api.routes.feature_flags.controllers.create_feature_flag import CreateFeatureFlagController
from app.api.routes.feature_flags.controllers.delete_feature_flag import DeleteFeatureFlagController
from app.api.routes.feature_flags.controllers.get_feature_flag import GetFeatureFlagController
from app.api.routes.feature_flags.controllers.get_feature_flag_audit_logs import GetFeatureFlagAuditLogsController
from app.api.routes.feature_flags.controllers.get_feature_flags import GetFeatureFlagsController
from app.api.routes.feature_flags.controllers.update_feature_flag import UpdateFeatureFlagController
from app.api.routes.feature_flags.controllers.update_feature_flag_status import UpdateFeatureFlagStatusController
from app.api.routes.feature_flags.schemas import CreateOrUpdateFeatureFlag, FeatureFlag, FeatureFlags, \
    FeatureFlagAuditLogs, UpdateFeatureFlagStatus
from app.api.schemas import SuccessResponse, User
from app.constants import DEFAULT_PAGE_SIZE

router = APIRouter(
    prefix='/feature_flags',
    tags=['Feature Flags']
)


@router.get('', response_model=FeatureFlags)
def get_feature_flags(
    project_id: int,
    page: int = 0,
    page_size: int = DEFAULT_PAGE_SIZE
) -> FeatureFlags:
    return GetFeatureFlagsController(
        project_id=project_id,
        page=page,
        page_size=page_size
    ).handle_request()


@router.post('', response_model=FeatureFlag)
def create_feature_flag(
    project_id: int,
    request: CreateOrUpdateFeatureFlag,
    me: User = Depends(auth.get_user)
) -> FeatureFlag:
    return CreateFeatureFlagController(
        project_id=project_id,
        request=request,
        me=me
    ).handle_request()


@router.get('/{feature_flag_id}', response_model=FeatureFlag)
def get_feature_flag(project_id: int, feature_flag_id: int) -> FeatureFlag:
    return GetFeatureFlagController(
        project_id=project_id,
        feature_flag_id=feature_flag_id
    ).handle_request()


@router.put('/{feature_flag_id}', response_model=FeatureFlag)
def update_feature_flag(
    project_id: int,
    feature_flag_id: int,
    request: CreateOrUpdateFeatureFlag,
    me: User = Depends(auth.get_user)
) -> FeatureFlag:
    return UpdateFeatureFlagController(
        project_id=project_id,
        feature_flag_id=feature_flag_id,
        request=request,
        me=me
    ).handle_request()


@router.delete('/{feature_flag_id}', response_model=SuccessResponse)
def delete_feature_flag(
    project_id: int,
    feature_flag_id: int,
    me: User = Depends(auth.get_user)
) -> SuccessResponse:
    return DeleteFeatureFlagController(
        project_id=project_id,
        feature_flag_id=feature_flag_id,
        me=me
    ).handle_request()


@router.get('/{feature_flag_id}/audit_logs', response_model=FeatureFlagAuditLogs)
def get_feature_flag_audit_logs(
    project_id: int,
    feature_flag_id: int,
    page: int = 0,
    page_size: int = DEFAULT_PAGE_SIZE,
    me: User = Depends(auth.get_user)
) -> FeatureFlagAuditLogs:
    return GetFeatureFlagAuditLogsController(
        project_id=project_id,
        feature_flag_id=feature_flag_id,
        page=page,
        page_size=page_size,
        me=me
    ).handle_request()


@router.put('/{feature_flag_id}/status', response_model=SuccessResponse)
def update_feature_flag_status(
    project_id: int,
    feature_flag_id: int,
    request: UpdateFeatureFlagStatus,
    me: User = Depends(auth.get_user)
) -> SuccessResponse:
    return UpdateFeatureFlagStatusController(
        project_id=project_id,
        feature_flag_id=feature_flag_id,
        request=request,
        me=me
    ).handle_request()
