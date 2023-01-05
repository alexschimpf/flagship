from fastapi import APIRouter

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('')
async def get_users() -> str:
    return 'Ok'


@router.post('')
async def create_user() -> str:
    return 'Ok'


@router.get('/{user_id}')
async def get_user(user_id: int) -> str:
    return 'Ok'


@router.put('/{user_id}')
async def update_user(user_id: int) -> str:
    return 'Ok'


@router.delete('/{user_id}')
async def delete_user(user_id: int) -> str:
    return 'Ok'
