import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class Config:

    SECRET_KEY: str
    MYSQL_ECHO: bool
    MYSQL_ISOLATION_LEVEL: str
    MYSQL_POOL_SIZE: int
    MYSQL_MAX_OVERFLOW: int
    MYSQL_CONN_STR: str
    REDIS_CONN_STR: str
    UI_BASE_URL: str
    SESSION_COOKIE_KEY: str
    SESSION_COOKIE_MAX_AGE: int
    SESSION_COOKIE_DOMAIN: str
    CORS_ALLOW_ORIGINS: list[str]
    SET_PASSWORD_TOKEN_TTL: int
    ENABLE_FAKE_AUTH: bool
    DEFAULT_LOCALE: str

    @classmethod
    def init(cls) -> None:
        cls.SECRET_KEY = cls._get_value(
            env_var='SECRET_KEY', default='_NOR3QX7-7LAJLLQ_OeOMuFzfq1Xg9RICwTalktXg5s=', warn_if_missing=True)
        cls.MYSQL_ECHO = cls._get_value(
            env_var='MYSQL_ECHO', default=True, type_cast=cls._to_bool, warn_if_missing=True)
        cls.MYSQL_ISOLATION_LEVEL = cls._get_value(
            env_var='MYSQL_ISOLATION_LEVEL', default='READ COMMITTED')
        cls.MYSQL_POOL_SIZE = cls._get_value(
            env_var='MYSQL_POOL_SIZE', default=5)
        cls.MYSQL_MAX_OVERFLOW = cls._get_value(
            env_var='MYSQL_MAX_OVERFLOW', default=10)
        cls.MYSQL_CONN_STR = cls._get_value(
            env_var='MYSQL_CONN_STR', default='mysql+mysqlconnector://root:test@localhost:3306/flagship',
            warn_if_missing=True)
        cls.REDIS_CONN_STR = cls._get_value(
            env_var='REDIS_CONN_STR', default='redis://redis:7000',
            warn_if_missing=True)
        cls.UI_BASE_URL = cls._get_value(
            env_var='UI_BASE_URL', default='http://localhost:3000', warn_if_missing=True)
        cls.SESSION_COOKIE_KEY = cls._get_value(
            env_var='SESSION_COOKIE_KEY', default='flagship-session')
        cls.SESSION_COOKIE_MAX_AGE = cls._get_value(
            env_var='COOKIE_MAX_AGE', default=86400)
        cls.SESSION_COOKIE_DOMAIN = cls._get_value(
            env_var='SESSION_COOKIE_DOMAIN', default='localhost', warn_if_missing=True)
        cls.CORS_ALLOW_ORIGINS = cls._get_value(
            env_var='CORS_ALLOW_ORIGINS', default='http://localhost:3000', warn_if_missing=True, type_cast=cls._to_str_list)
        cls.SET_PASSWORD_TOKEN_TTL = cls._get_value(
            env_var='SET_PASSWORD_TOKEN_TTL', default=86400)
        cls.ENABLE_FAKE_AUTH = cls._get_value(
            env_var='ENABLE_FAKE_AUTH', default=False, type_cast=cls._to_bool)
        cls.DEFAULT_LOCALE = cls._get_value(
            env_var='DEFAULT_LOCALE', default='en-us')

    @staticmethod
    def _to_bool(val: Any) -> bool:
        if isinstance(val, bool):
            return val
        if not val or (val.lower() in ('false', 'no', '0')):
            return False

        return True

    @staticmethod
    def _to_str_list(val: str) -> list[str]:
        if not val:
            return []

        return val.split(',')

    @staticmethod
    def _get_value(env_var: str, default: Any, type_cast: Any = None, warn_if_missing: bool = False) -> Any:
        value: Any = os.getenv(env_var)
        if value is None:
            if warn_if_missing:
                logger.warning(f'Default value used for "{env_var}" environment variable. '
                               f'This is not recommended for production!')
            value = default
        if type_cast:
            value = type_cast(value)

        return value
