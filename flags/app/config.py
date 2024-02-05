import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class Config:

    SECRET_KEY: str
    REDIS_CONN_STR: str
    CORS_ALLOW_ORIGINS: list[str]
    DEFAULT_LOCALE: str

    @classmethod
    def init(cls) -> None:
        cls.SECRET_KEY = cls._get_value(
            env_var='SECRET_KEY', default='_NOR3QX7-7LAJLLQ_OeOMuFzfq1Xg9RICwTalktXg5s=', warn_if_missing=True)
        cls.REDIS_CONN_STR = cls._get_value(
            env_var='REDIS_CONN_STR', default='redis://127.0.0.1:7000',
            warn_if_missing=True)
        cls.CORS_ALLOW_ORIGINS = cls._get_value(
            env_var='CORS_ALLOW_ORIGINS', default='*', warn_if_missing=True, type_cast=cls._to_str_list)
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
