from typing import Any, cast
from fastapi import APIRouter
from bson import ObjectId

from app.services.database.mongodb import types, collections
from app.api.routes import schemas
from app.api import exceptions

router = APIRouter(
    prefix='/feature-flags',
    tags=['Feature Flags']
)


@router.get('', response_model=schemas.FeatureFlags)
async def get_feature_flags(
    project_id: str
) -> Any:
    feature_flags = collections.projects.get_feature_flags(project_id=ObjectId(project_id))
    if feature_flags is None:
        raise exceptions.NotFoundException

    return schemas.FeatureFlags(feature_flags=[
        schemas.FeatureFlag.from_raw(raw=feature_flag)
        for feature_flag in feature_flags
    ])


@router.post('', response_model=schemas.FeatureFlag)
async def create_feature_flag(
    project_id: str,
    request: schemas.CreateOrUpdateFeatureFlag
) -> Any:
    feature_flag_id, project_found = collections.projects.create_feature_flag(
        project_id=ObjectId(project_id),
        name=request.name,
        description=request.description,
        enabled=request.enabled,
        conditions=[
            [
                {
                    'context_key': condition.context_key,
                    'operator': condition.operator,
                    'value': condition.value
                }
                for condition in group
            ] for group in request.conditions
        ]
    )
    if not project_found:
        raise exceptions.NotFoundException

    feature_flag = cast(types.FeatureFlag, collections.projects.get_feature_flag(
        project_id=ObjectId(project_id), feature_flag_id=feature_flag_id
    ))
    return schemas.FeatureFlag.from_raw(raw=feature_flag)


@router.get('/{feature_flag_id}', response_model=schemas.FeatureFlag)
async def get_feature_flag(
    project_id: str,
    feature_flag_id: str
) -> Any:
    feature_flag = collections.projects.get_feature_flag(
        project_id=ObjectId(project_id), feature_flag_id=ObjectId(feature_flag_id)
    )
    if not feature_flag:
        raise exceptions.NotFoundException
    return schemas.FeatureFlag.from_raw(raw=feature_flag)


@router.put('/{feature_flag_id}', response_model=schemas.FeatureFlag)
async def update_feature_flag(
    project_id: str,
    feature_flag_id: str,
    request: schemas.CreateOrUpdateFeatureFlag
) -> Any:
    matched = collections.projects.update_feature_flag(
        project_id=ObjectId(project_id),
        feature_flag_id=ObjectId(feature_flag_id),
        name=request.name,
        description=request.description,
        enabled=request.enabled,
        conditions=[
            [
                {
                    'context_key': condition.context_key,
                    'operator': condition.operator,
                    'value': condition.value
                }
                for condition in group
            ] for group in request.conditions
        ]
    )
    if not matched:
        raise exceptions.NotFoundException

    feature_flag = cast(types.FeatureFlag, collections.projects.get_feature_flag(
        project_id=ObjectId(project_id), feature_flag_id=ObjectId(feature_flag_id)
    ))
    return schemas.FeatureFlag.from_raw(raw=feature_flag)


@router.delete('/{feature_flag_id}', response_model=schemas.SuccessResponse)
async def delete_feature_flag(
    project_id: str,
    feature_flag_id: str
) -> Any:
    deleted = collections.projects.delete_feature_flag(
        project_id=ObjectId(project_id),
        feature_flag_id=ObjectId(feature_flag_id)
    )
    if not deleted:
        raise exceptions.NotFoundException

    return schemas.SuccessResponse(success=True)
