from typing import Any
from fastapi.responses import RedirectResponse
from fastapi import APIRouter

from app.api.routes.auth.controllers.login import LoginController
from app.api.routes.auth.controllers.logout import LogoutController

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/', response_class=RedirectResponse, include_in_schema=False)
def login(email: str, password: str, authorize: Any) -> Any:
    return LoginController().handle_request()


@router.post('/', response_class=RedirectResponse, include_in_schema=False)
def logout() -> Any:
    return LogoutController().handle_request()
