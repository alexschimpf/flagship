import secrets

from cryptography import fernet

from app.config import Config


def generate_private_key() -> tuple[str, str]:
    private_key = secrets.token_hex()
    f = fernet.Fernet(Config.SECRET_KEY.encode())
    encrypted_private_key = f.encrypt(private_key.encode()).decode()
    return private_key, encrypted_private_key
