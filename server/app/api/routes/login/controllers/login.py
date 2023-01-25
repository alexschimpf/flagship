import bcrypt
import urllib.parse
from typing import Any, cast
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi_jwt_auth import AuthJWT

from app.api import exceptions
from app.services.database.mongodb import collections
from app.services.database.mongodb.types import UserStatus
from app import config


def process(
    email: str,
    password: str,
    authorize: AuthJWT
) -> Any:
    access_token: str
    try:
        user = collections.users.get_user_by_email(email=email)
        if not user or user['status'] != UserStatus.ACTIVATED:
            raise exceptions.InvalidLoginCredentialsException

        attempted_password = password.encode('utf-8')
        hashed_password = cast(str, user['password']).encode('utf-8')
        if bcrypt.hashpw(attempted_password, hashed_password) != hashed_password:
            raise exceptions.InvalidLoginCredentialsException

        access_token = authorize.create_access_token(subject=str(user['_id']))
    except Exception as e:
        error = urllib.parse.quote(
           str(e) if isinstance(e, exceptions.AppException) else exceptions.AppException.DEFAULT_MESSAGE
        )
        return RedirectResponse(
            url=f'{config.UI_BASE_URL}/login?error={error}',
            status_code=status.HTTP_302_FOUND
        )

    response = RedirectResponse(
        url=config.UI_BASE_URL,
        status_code=status.HTTP_302_FOUND
    )
    response.set_cookie(
        key='fs-access-token',
        value=access_token
    )
    return response
