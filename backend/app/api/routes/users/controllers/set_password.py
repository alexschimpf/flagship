import time
import urllib.parse
from typing import cast

import bcrypt
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi_another_jwt_auth import AuthJWT

from app.api.exceptions.exceptions import InvalidPasswordException, InvalidSetPasswordTokenException, AppException, \
    PasswordsDontMatchException
from app.api.routes.users.schemas import SetPassword
from app.config import Config
from app.constants import AuditLogEventType
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogRow
from app.services.database.mysql.schemas.user import UserRow, UsersTable
from app.services.database.mysql.service import MySQLService
from app.services.strings.service import StringsService


class SetPasswordController:

    def __init__(self, email: str, password: str, password_repeat: str, token: str, authorize: AuthJWT):
        self.email = email
        self.password = password
        self.password_repeat = password_repeat
        self.token = token
        self.authorize = authorize

    def handle_request(self) -> RedirectResponse:
        try:
            user = self._get_user_by_email(email=self.email)
            self._validate(user=user)
            if user:
                self._update_password(user=user)
        except Exception as e:
            error = urllib.parse.quote(
                str(e) if isinstance(e, AppException) else StringsService.get(key=AppException.CODE)
            )
            return RedirectResponse(
                url=f'{Config.UI_BASE_URL}/set-password?error={error}&token={self.token}',
                status_code=status.HTTP_302_FOUND
            )
        else:
            access_token = self.authorize.create_access_token(subject=cast(UserRow, user).user_id)
            response = RedirectResponse(
                url=Config.UI_BASE_URL,
                status_code=status.HTTP_302_FOUND
            )
            response.set_cookie(
                key=Config.SESSION_COOKIE_KEY,
                value=access_token,
                max_age=Config.SESSION_COOKIE_MAX_AGE,
                domain=Config.SESSION_COOKIE_DOMAIN,
                secure=True,
                samesite='lax'
            )
            return response

    def _validate(self, user: UserRow | None) -> None:
        if self.password != self.password_repeat:
            raise PasswordsDontMatchException

        if not user or not user.set_password_token:
            raise InvalidSetPasswordTokenException

        hashed_token, expire_time = user.set_password_token.split('|')
        if not bcrypt.checkpw(self.token.encode(), hashed_token.encode()):
            raise InvalidSetPasswordTokenException
        if time.time() > float(expire_time):
            raise InvalidSetPasswordTokenException

        if not self.is_password_valid():
            raise InvalidPasswordException(field='password')

    def is_password_valid(self) -> bool:
        password = self.password

        if len(password) < 8:
            return False

        has_one_uppercase_letter = False
        has_one_lowercase_letter = False
        has_one_number = False
        has_one_special_char = False
        for c in password:
            if c.isspace():
                return False
            if c.islower():
                has_one_lowercase_letter = True
            elif c.isupper():
                has_one_uppercase_letter = True
            elif c.isdigit():
                has_one_number = True
            else:
                has_one_special_char = True

        return (
            has_one_uppercase_letter and
            has_one_lowercase_letter and
            has_one_number and
            has_one_special_char
        )

    def _update_password(self, user: UserRow) -> None:
        hashed_password = bcrypt.hashpw(
            self.password.encode(),
            bcrypt.gensalt(prefix=b'2a')
        ).decode()
        with MySQLService.get_session() as session:
            UsersTable.update_password(
                user_id=user.user_id,
                password=hashed_password,
                session=session
            )
            session.add(SystemAuditLogRow(
                actor=self.email,
                event_type=AuditLogEventType.SET_PASSWORD
            ))
            session.commit()

    @staticmethod
    def _get_user_by_email(email: str) -> UserRow | None:
        with MySQLService.get_session() as session:
            user_row = UsersTable.get_user_by_email(email=email, session=session)

        return user_row
