from typing import Any
from bson import ObjectId
from fastapi.responses import JSONResponse

from app.services.database.mongodb import types, collections
from app.api.routes.users.controllers import common
from app.api.routes.users import schemas
from app.api.schemas import SuccessResponse
from app.api import exceptions


def process(
    request: schemas.SetPassword
) -> Any:
    # TODO: Token should expire
    # TODO: Should have minimum requirements for password
    user = collections.users.get_user_by_email(email=request.email)
    if not user:
        raise Exception

    errors: list[exceptions.AppException] = []
    common.validate_password(password=request.password, errors=errors)
    _validate_token(user=user, token=request.token, errors=errors)

    if errors:
        raise exceptions.AggregateException(exceptions=errors)

    collections.users.update_user_password(
        user_id=ObjectId(user['_id']),
        password=request.password
    )

    '''
    TODO: Redirect to home page and set JWT cookies
    access_token = ''
    refresh_token = ''
    '''
    return JSONResponse(
        content=SuccessResponse(success=True).dict(),
        headers={
        }
    )


def _validate_token(user: types.User, token: str, errors: list[exceptions.AppException]) -> None:
    # TODO: This token should be hashed
    if user['password_token'] != token:
        errors.append(exceptions.InvalidSetPasswordAttemptException(field='token'))
