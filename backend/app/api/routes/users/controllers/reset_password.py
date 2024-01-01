import secrets

from app.api.routes.users.schemas import ResetPassword
from app.api.schemas import SuccessResponse
from app.services.database.mysql.schemas.user import UsersTable
from app.services.database.mysql.service import MySQLService


class ResetPasswordController:

    def __init__(self, request: ResetPassword):
        self.request = request

    def handle_request(self) -> SuccessResponse:
        set_password_token = secrets.token_urlsafe()
        with MySQLService.get_session() as session:
            UsersTable.update_set_password_token(
                email=self.request.email,
                set_password_token=set_password_token,
                session=session
            )
            session.commit()

        return SuccessResponse()
