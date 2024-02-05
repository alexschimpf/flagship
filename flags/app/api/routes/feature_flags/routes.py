from fastapi import Request, Header, APIRouter

from app.api.routes.feature_flags.schemas import FeatureFlags
from app.api.routes.feature_flags.controllers.get_feature_flags import GetFeatureFlagsController

router = APIRouter(
    prefix='/feature_flags',
    tags=['Feature Flags']
)


@router.post('', response_model=FeatureFlags)
def get_enabled_feature_flags(
    project_id: int,
    user_key: str,
    request: Request,
    signature: str = Header()
) -> FeatureFlags:
    context = request.json
    return GetFeatureFlagsController(
        project_id=project_id,
        user_key=user_key,
        context=context,
        signature=signature
    ).handle_request()
