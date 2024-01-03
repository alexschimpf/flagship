from typing import Any

from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi_another_jwt_auth import AuthJWT

from app.api.routes.auth.controllers.login import LoginController
from app.api.routes.auth.controllers.logout import LogoutController
from app.api.schemas import SuccessResponse

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/login', response_class=RedirectResponse, include_in_schema=False)
def login(email: str = Form(), password: str = Form(), authorize: AuthJWT = Depends()) -> RedirectResponse:
    return LoginController(
        email=email,
        password=password,
        authorize=authorize
    ).handle_request()


@router.post('/login/test', response_class=RedirectResponse, include_in_schema=False)
def login_test(authorize: AuthJWT = Depends()) -> Any:
    authorize.jwt_required()
    return SuccessResponse(success=True)


@router.post('/logout', response_class=RedirectResponse, include_in_schema=False)
def logout() -> Any:
    return LogoutController().handle_request()


