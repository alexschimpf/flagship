from typing import Any
from fastapi import APIRouter

from app.api.routes.feature_flags import schemas
from app.api.schemas import SuccessResponse
from app.api.routes.feature_flags import controllers

router = APIRouter(
    prefix='/feature-flags',
    tags=['Feature Flags']
)


@router.get('', response_model=schemas.FeatureFlags)
def get_feature_flags(
    project_id: str
) -> Any:
    return controllers.get_feature_flags.process(project_id=project_id)


@router.post('', response_model=schemas.FeatureFlag)
def create_feature_flag(
    project_id: str,
    request: schemas.CreateOrUpdateFeatureFlag
) -> Any:
    return controllers.create_feature_flag.process(
        project_id=project_id, request=request)


@router.get('/{feature_flag_id}', response_model=schemas.FeatureFlag)
def get_feature_flag(
    project_id: str,
    feature_flag_id: str
) -> Any:
    return controllers.get_feature_flag.process(
        project_id=project_id, feature_flag_id=feature_flag_id)


@router.put('/{feature_flag_id}', response_model=schemas.FeatureFlag)
def update_feature_flag(
    project_id: str,
    feature_flag_id: str,
    request: schemas.CreateOrUpdateFeatureFlag
) -> Any:
    return controllers.update_feature_flag.process(
        project_id=project_id, feature_flag_id=feature_flag_id, request=request)


@router.delete('/{feature_flag_id}', response_model=SuccessResponse)
def delete_feature_flag(
    project_id: str,
    feature_flag_id: str
) -> Any:
    controllers.delete_feature_flag.process(
        project_id=project_id, feature_flag_id=feature_flag_id)
