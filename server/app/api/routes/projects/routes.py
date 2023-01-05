from fastapi import APIRouter

router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.get('')
async def get_projects() -> str:
    return 'Ok'


@router.post('')
async def create_project() -> str:
    return 'Ok'


@router.get('/{project_id}')
async def get_project(project_id: int) -> str:
    return 'Ok'


@router.put('/{project_id}')
async def update_project(project_id: int) -> str:
    return 'Ok'


@router.delete('/{project_id}')
async def delete_project(project_id: int) -> str:
    return 'Ok'
