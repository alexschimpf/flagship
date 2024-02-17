from app.api.routes.users.controllers import common
from app.api.routes.users.schemas import ResetPassword
from app.api.schemas import SuccessResponse
from app.constants import AuditLogEventType
from app.services.database.mysql.schemas.system_audit_logs import SystemAuditLogRow
from app.services.database.mysql.schemas.user import UsersTable
from app.services.database.mysql.service import MySQLService
from app.services.email.service import EmailService, Templates
from app.config import Config


class ResetPasswordController:
    def __init__(self, request: ResetPassword):
        self.request = request

    def handle_request(self) -> SuccessResponse:
        hashed_set_password_token, token = common.generate_set_password_token()
        with MySQLService.get_session() as session:
            UsersTable.update_set_password_token(
                email=self.request.email, set_password_token=hashed_set_password_token, session=session
            )
            session.add(SystemAuditLogRow(actor=self.request.email, event_type=AuditLogEventType.RESET_PASSWORD))
            session.commit()

        EmailService.send_email(
            subject='Flagship - Reset Password',
            to=self.request.email,
            template=Templates.RESET_PASSWORD,
            template_vars={'url': f'{Config.UI_BASE_URL}/set-password?token={token}'},
        )

        return SuccessResponse()
