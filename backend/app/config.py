import os
import logging
from typing import Any

logger = logging.getLogger(__name__)


class Config:

    SECRET_KEY: str
    MYSQL_ECHO: bool
    MYSQL_ISOLATION_LEVEL: str
    MYSQL_POOL_SIZE: int
    MYSQL_MAX_OVERFLOW: int
    MYSQL_CONN_STR: str

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

    @staticmethod
    def _to_bool(val: Any) -> bool:
        if not val or (isinstance(val, str) and val.lower() in ('false', 'no')):
            return False

        return True

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
