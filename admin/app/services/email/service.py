import os
import smtplib
import logging
from email.message import EmailMessage

from app.config import Config

logger = logging.getLogger(__name__)

class Templates:
    INVITE_USER = 'invite-user.html'
    RESET_PASSWORD = 'reset-password.html'


class EmailService:

    @staticmethod
    def send_email(
        subject: str,
        to: str,
        body: str | None = None,
        template: str | None = None,
        template_vars: dict[str, str] | None = None
    ) -> None:
        if not Config.SMTP_HOST:
            logger.info('Skipping email...')
            return

        server = smtplib.SMTP_SSL(host=Config.SMTP_HOST, port=Config.SMTP_PORT)
        try:
            server.ehlo()
            server.login(user=Config.SMTP_HOST, password=Config.SMTP_PASSWORD)

            message = EmailMessage()
            message['Subject'] = subject
            message['From'] = Config.EMAIL_FROM_ADDRESS
            message['To'] = to

            if body:
                message.set_content(body)
            if template:
                template_path = os.path.join(os.path.dirname(__file__), 'templates', template)
                with open(template_path, 'r') as template_file:
                    template_content = template_file.read()
                    if template_vars:
                        for k, v in template_vars.items():
                            template_content.replace(f'%%{k.upper()}%%', v)
                    message.set_content(template_content)

            server.send_message(message)
        finally:
            server.quit()
