from typing import Any

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from app import config


class MySQLService:

    _engine: Engine

    @classmethod
    def init(cls) -> None:
        cls._engine = create_engine(
            url=config.MYSQL_CONN_STR,
            echo=config.MYSQL_ECHO,
            echo_pool=config.MYSQL_ECHO,
            isolation_level=config.MYSQL_ISOLATION_LEVEL,
            pool_size=config.MYSQL_POOL_SIZE,
            max_overflow=config.MYSQL_MAX_OVERFLOW
        )

    @classmethod
    def get_session(cls, expire_on_commit: bool = False, **kwargs: Any) -> Session:
        return Session(bind=cls._engine, expire_on_commit=expire_on_commit, **kwargs)
