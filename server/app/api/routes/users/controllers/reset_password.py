from typing import Any
import secrets
import urllib.parse
from fastapi.responses import RedirectResponse

from app import config
from app.services.database.mongodb import collections


def process(
    email: str
) -> Any:
    user = collections.users.get_user_by_email(email=email)
    if user:
        token = secrets.token_urlsafe()
        collections.users.update_user_password_token(
            user_id=user['_id'],
            password_token=token
        )
        # TODO: Send password reset email

    params = urllib.parse.urlencode({
        'message': 'A password reset confirmation email has been sent to your inbox.'
    })
    return RedirectResponse(f'{config.UI_BASE_URL}/login?{params}')
