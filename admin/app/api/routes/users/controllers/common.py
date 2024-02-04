import secrets
import time

import bcrypt

from app.config import Config


def generate_set_password_token() -> tuple[str, str]:
    token = secrets.token_urlsafe().encode()
    hashed_token = bcrypt.hashpw(
        token,
        bcrypt.gensalt(prefix=b'2a')
    ).decode()
    expire_time = time.time() + Config.SET_PASSWORD_TOKEN_TTL  # expire in 24 hours
    set_password_token = '|'.join((
        hashed_token,
        str(expire_time)
    ))

    return set_password_token, token.decode()
