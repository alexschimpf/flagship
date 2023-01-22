from typing import Any
from fastapi import APIRouter

from app.api.schemas import SuccessResponse

router = APIRouter(
    prefix='/login',
    tags=['Login']
)


@router.get('/test', response_model=SuccessResponse)
def get_login_test() -> Any:
    return SuccessResponse(success=True)
