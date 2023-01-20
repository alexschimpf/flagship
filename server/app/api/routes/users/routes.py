from typing import Any
from fastapi import APIRouter

from app.api.routes.users import controllers, schemas
from app.api.schemas import SuccessResponse

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.put('/password', response_model=SuccessResponse)
def set_password(
    request: schemas.SetPassword
) -> Any:
    return controllers.set_password.process(request=request)


@router.post('/password/reset', response_model=SuccessResponse)
def reset_password(
    request: schemas.ResetPassword
) -> Any:
    return controllers.reset_password.process(request=request)


@router.get('', response_model=schemas.Users)
def get_users() -> Any:
    return controllers.get_users.process()


@router.post('', response_model=schemas.User)
def invite_user(
    request: schemas.InviteUser
) -> Any:
    return controllers.invite_user.process(request=request)


@router.get('/{user_id}', response_model=schemas.User)
def get_user(
    user_id: str
) -> Any:
    return controllers.get_user.process(user_id=user_id)


@router.put('/{user_id}', response_model=schemas.User)
def update_user(
    user_id: str,
    request: schemas.UpdateUser
) -> Any:
    return controllers.update_user.process(user_id=user_id, request=request)


@router.delete('/{user_id}', response_model=SuccessResponse)
def delete_user(
    user_id: str
) -> Any:
    return controllers.delete_user.process(user_id=user_id)
