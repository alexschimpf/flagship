from typing import Any
from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi_jwt_auth import AuthJWT

from app.api.routes.login import controllers
from app.api.schemas import SuccessResponse

router = APIRouter(
    prefix='/login',
    tags=['Login']
)


@router.post('/', response_class=RedirectResponse, include_in_schema=False)
def login(
    email: str = Form(),
    password: str = Form(),
    authorize: AuthJWT = Depends()
) -> Any:
    return controllers.login.process(
        email=email,
        password=password,
        authorize=authorize
    )


@router.get('/test', response_model=SuccessResponse)
def get_login_test(authorize: AuthJWT = Depends()) -> Any:
    authorize.jwt_required()
    return SuccessResponse(success=True)
