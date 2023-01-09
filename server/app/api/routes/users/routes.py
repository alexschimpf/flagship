from fastapi import APIRouter

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('')
def get_users() -> str:
    return 'Ok'


@router.post('')
def create_user() -> str:
    return 'Ok'


@router.get('/{user_id}')
def get_user(user_id: int) -> str:
    return 'Ok'


@router.put('/{user_id}')
def update_user(user_id: int) -> str:
    return 'Ok'


@router.delete('/{user_id}')
def delete_user(user_id: int) -> str:
    return 'Ok'
