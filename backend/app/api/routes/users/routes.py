from fastapi import APIRouter, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi_another_jwt_auth import AuthJWT

from app.api import auth
from app.api.routes.users.controllers.delete_user import DeleteUserController
from app.api.routes.users.controllers.get_user import GetUserController
from app.api.routes.users.controllers.get_users import GetUsersController
from app.api.routes.users.controllers.invite_user import InviteUserController
from app.api.routes.users.controllers.reset_password import ResetPasswordController
from app.api.routes.users.controllers.set_password import SetPasswordController
from app.api.routes.users.controllers.update_user import UpdateUserController
from app.api.routes.users.schemas import SetPassword, ResetPassword, InviteUser, UpdateUser, Users
from app.api.schemas import SuccessResponse, User
from app.constants import DEFAULT_PAGE_SIZE

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.put('/password', response_class=RedirectResponse)
def set_password(request: SetPassword, authorize: AuthJWT = Depends()) -> RedirectResponse:
    return SetPasswordController(
        request=request,
        authorize=authorize
    ).handle_request()


@router.post('/password/reset', response_model=SuccessResponse)
def reset_password(request: ResetPassword) -> SuccessResponse:
    return ResetPasswordController(
        request=request
    ).handle_request()


@router.get('', response_model=Users)
def get_users(
    page: int = 0,
    page_size: int = DEFAULT_PAGE_SIZE,
    me: User = Depends(auth.get_user)
) -> Users:
    return GetUsersController(
        page=page,
        page_size=page_size,
        me=me
    ).handle_request()


@router.post('', response_model=User)
def invite_user(request: InviteUser, me: User = Depends(auth.get_user)) -> User:
    return InviteUserController(
        request=request,
        me=me
    ).handle_request()


@router.get('/me', response_model=User)
def get_me(me: User = Depends(auth.get_user)) -> User:
    return me


@router.get('/{user_id}', response_model=User)
def get_user(user_id: int, me: User = Depends(auth.get_user)) -> User:
    return GetUserController(
        user_id=user_id,
        me=me
    ).handle_request()


@router.put('/{user_id}', response_model=User)
def update_user(user_id: int, request: UpdateUser, me: User = Depends(auth.get_user)) -> User:
    return UpdateUserController(
        user_id=user_id,
        request=request,
        me=me
    ).handle_request()


@router.delete('/{user_id}', response_model=SuccessResponse)
def delete_user(
    user_id: int,
    response: Response,
    me: User = Depends(auth.get_user)
) -> SuccessResponse:
    return DeleteUserController(
        user_id=user_id,
        me=me
    ).handle_request(response=response)
