import bcrypt

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

        return SuccessResponse()

    def _validate(self, user: UserRow) -> None:
        if not user or user.set_password_token != self.request.token:
            raise Exception('User not found')

        # TODO: Validate password

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
