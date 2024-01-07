import urllib.parse

import bcrypt
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi_another_jwt_auth import AuthJWT

from app.api import exceptions
from app.config import Config
from app.constants import UserStatus
from app.services.database.mysql.schemas.user import UsersTable
from app.services.database.mysql.service import MySQLService


class LoginController:

    def __init__(self, email: str, password: str, authorize: AuthJWT) -> None:
        self.email = email
        self.password = password
        self.authorize = authorize

    def handle_request(self) -> RedirectResponse:
        access_token: str
        try:
            with MySQLService.get_session() as session:
                user = UsersTable.get_user_by_email(email=self.email, session=session)

            if user.status != UserStatus.ACTIVATED.value:
                raise exceptions.UserNotActivatedException
            if not user:
                raise exceptions.InvalidLoginCredentialsException

            attempted_password = self.password.encode()
            hashed_password = user.password.encode()
            if not bcrypt.checkpw(attempted_password, hashed_password):
                raise exceptions.InvalidLoginCredentialsException

            access_token = self.authorize.create_access_token(subject=user.user_id)
        except Exception as e:
            error = urllib.parse.quote(
                str(e) if isinstance(e, exceptions.AppException) else exceptions.AppException.DEFAULT_MESSAGE
            )
            return RedirectResponse(
                url=f'{Config.UI_BASE_URL}/login?error={error}',
                status_code=status.HTTP_302_FOUND
            )

        response = RedirectResponse(
            url=Config.UI_BASE_URL,
            status_code=status.HTTP_302_FOUND
        )

        response.set_cookie(
            key=Config.SESSION_COOKIE_KEY,
            value=access_token,
            max_age=Config.SESSION_COOKIE_MAX_AGE,
            domain=Config.SESSION_COOKIE_DOMAIN,
            secure=True
        )
        return response
