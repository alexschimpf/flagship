import bcrypt

from app.api.exceptions.exceptions import InvalidPasswordException
from app.api.routes.users.schemas import SetPassword
from app.api.schemas import SuccessResponse
from app.services.database.mysql.schemas.user import UserRow, UsersTable
from app.services.database.mysql.service import MySQLService


class SetPasswordController:

    def __init__(self, request: SetPassword):
        self.request = request

    def handle_request(self) -> SuccessResponse:
        user = self._get_user_by_email(email=self.request.email)
        if user:
            self._validate(user=user)
            self._update_password(user=user)

        # TODO: Set JWT token so user is logged in

        return SuccessResponse()

    def _validate(self, user: UserRow) -> None:
        # TODO: Token should expire and be hashed
        if not user:
            raise Exception('User not found')
        if user.set_password_token != self.request.token:
            raise Exception('Set password token not valid')

        if not self.is_password_valid():
            raise InvalidPasswordException(field='password')

    def is_password_valid(self) -> bool:
        password = self.request.password

        if len(password) < 8:
            return False

        has_one_uppercase_letter = False
        has_one_lowercase_letter = False
        has_one_number = False
        has_one_special_char = False
        for c in password:
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
            self.request.password.encode('utf-8'),
            bcrypt.gensalt(prefix=b'2a')
        ).decode('utf-8')
        with MySQLService.get_session() as session:
            UsersTable.update_password(
                user_id=user.user_id,
                password=hashed_password,
                session=session
            )
            session.commit()

    @staticmethod
    def _get_user_by_email(email: str) -> UserRow | None:
        with MySQLService.get_session() as session:
            user_row = UsersTable.get_user_by_email(email=email, session=session)

        return user_row
