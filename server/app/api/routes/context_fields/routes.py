from fastapi import APIRouter

router = APIRouter(
    prefix='/context-fields',
    tags=['Context Fields']
)


@router.get('')
async def get_context_fields(project_id: int) -> str:
    return 'Ok'


@router.post('')
async def create_context_field(project_id: int) -> str:
    return 'Ok'


@router.get('/{context_field_id}')
async def get_context_field(project_id: int, context_field_id: int) -> str:
    return 'Ok'


@router.put('/{context_field_id}')
async def update_context_field(project_id: int, context_field_id: int) -> str:
    return 'Ok'


@router.delete('/{context_field_id}')
async def delete_context_field(project_id: int, context_field_id: int) -> str:
    return 'Ok'
