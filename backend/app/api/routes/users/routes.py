from typing import Any
from fastapi import APIRouter

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.put('/password')
def set_password(request: Any) -> Any:
    pass


@router.post('/password/reset')
def reset_password(request: Any) -> Any:
    pass


@router.get('')
def get_users() -> Any:
    pass


@router.post('')
def invite_user(request: Any) -> Any:
    pass


@router.get('/{user_id}')
def get_user(user_id: str) -> Any:
    pass


@router.put('/{user_id}')
def update_user(user_id: str, request: Any) -> Any:
    pass


@router.delete('/{user_id}')
def delete_user(user_id: str) -> Any:
    pass
