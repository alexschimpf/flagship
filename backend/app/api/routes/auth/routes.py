from typing import Any
from fastapi.responses import RedirectResponse
from fastapi import APIRouter

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/', response_class=RedirectResponse, include_in_schema=False)
def login(email: str, password: str, authorize: Any) -> Any:
    pass


@router.post('/', response_class=RedirectResponse, include_in_schema=False)
def logout() -> Any:
    pass
