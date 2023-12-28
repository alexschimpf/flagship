from typing import Any
from fastapi import APIRouter

router = APIRouter(
    prefix='/feature_flags',
    tags=['Feature Flags']
)


@router.get('')
def get_feature_flags(project_id: str) -> Any:
    pass


@router.post('')
def create_feature_flag(project_id: str, request: Any) -> Any:
    pass


@router.get('/{feature_flag_id}')
def get_feature_flag(project_id: str, feature_flag_id: str) -> Any:
    pass


@router.put('/{feature_flag_id}')
def update_feature_flag(project_id: str, feature_flag_id: str, request: Any) -> Any:
    pass


@router.delete('/{feature_flag_id}')
def delete_feature_flag(project_id: str, feature_flag_id: str) -> Any:
    pass
