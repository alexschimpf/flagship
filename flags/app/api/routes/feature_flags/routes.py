from typing import Any
from fastapi import Body, Header, APIRouter

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
    context: dict[str, Any] = Body(),
    flagship_signature: str = Header()
) -> FeatureFlags:
    return GetFeatureFlagsController(
        project_id=project_id,
        user_key=user_key,
        context=context,
        signature=flagship_signature
    ).handle_request()
