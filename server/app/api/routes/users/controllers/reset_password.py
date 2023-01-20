from typing import Any
import secrets

from app.services.database.mongodb import collections
from app.api.routes.users import schemas
from app.api.schemas import SuccessResponse


def process(
    request: schemas.ResetPassword
) -> Any:
    user = collections.users.get_user_by_email(email=request.email)
    if user:
        token = secrets.token_urlsafe()
        collections.users.update_user_password_token(
            user_id=user['_id'],
            password_token=token
        )
        # TODO: Send password reset email

    return SuccessResponse(success=True)
