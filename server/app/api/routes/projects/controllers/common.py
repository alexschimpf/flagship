import secrets
from cryptography import fernet

from app import config


def generate_private_key() -> tuple[str, str]:
    private_key = secrets.token_hex()
    f = fernet.Fernet(config.SECRET_KEY.encode())
    encrypted_private_key = f.encrypt(private_key.encode()).decode()
    return private_key, encrypted_private_key
