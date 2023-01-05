from fastapi import APIRouter

router = APIRouter(
    prefix='/feature-flags',
    tags=['Feature Flags']
)


@router.get('')
async def get_feature_flags(project_id: int) -> str:
    return 'Ok'


@router.post('')
async def create_feature_flag(project_id: int) -> str:
    return 'Ok'


@router.get('/{feature_flag_id}')
async def get_feature_flag(project_id: int, feature_flag_id: int) -> str:
    return 'Ok'


@router.put('/{feature_flag_id}')
async def update_feature_flag(project_id: int, feature_flag_id: int) -> str:
    return 'Ok'


@router.delete('/{feature_flag_id}')
async def delete_feature_flag(project_id: int, feature_flag_id: int) -> str:
    return 'Ok'
