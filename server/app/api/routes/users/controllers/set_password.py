from typing import Any
import urllib.parse
from bson import ObjectId
from fastapi.responses import RedirectResponse
import logging

from app.services.database.mongodb import types, collections
from app.api.routes.users.controllers import common
from app.api import exceptions
from app import config

logger = logging.getLogger(__name__)


def process(
    email: str,
    password: str,
    token: str
) -> Any:
    # TODO: Token should expire
    try:
        user = collections.users.get_user_by_email(email=email)
        if not user:
            raise Exception

        errors: list[exceptions.AppException] = []
        common.validate_password(password=password, errors=errors)
        _validate_token(user=user, token=token, errors=errors)

        if errors:
            raise exceptions.AggregateException(exceptions=errors)

        collections.users.update_user_password(
            user_id=ObjectId(user['_id']),
            password=password
        )
    except Exception as e:
        message = 'Sorry, an unexpected error occurred. Please try again.'
        if isinstance(e, exceptions.AppException):
            logger.exception(e)
            message = str(e)
        params = urllib.parse.urlencode({
            'error': message,
            'token': token
        })
        return RedirectResponse(url=f'{config.UI_BASE_URL}/set-password?{params}')

    '''
    TODO: Redirect to home page and set JWT cookies
    access_token = ''
    refresh_token = ''
    '''
    headers: dict[str, str] = {}
    return RedirectResponse(
        url=config.UI_BASE_URL,
        headers=headers
    )


def _validate_token(user: types.User, token: str, errors: list[exceptions.AppException]) -> None:
    if user['password_token'] != token:
        errors.append(exceptions.InvalidSetPasswordAttemptException(field='token'))
