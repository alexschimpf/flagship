from typing import Any

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from app.config import Config


class MySQLService:
    _engine: Engine

    @classmethod
    def init(cls) -> None:
        cls._engine = create_engine(
            url=Config.MYSQL_CONN_STR,
            echo=Config.MYSQL_ECHO,
            echo_pool=Config.MYSQL_ECHO,
            isolation_level=Config.MYSQL_ISOLATION_LEVEL,
            pool_size=Config.MYSQL_POOL_SIZE,
            max_overflow=Config.MYSQL_MAX_OVERFLOW,
        )

    @classmethod
    def get_session(cls, expire_on_commit: bool = False, **kwargs: Any) -> Session:
        return Session(bind=cls._engine, expire_on_commit=expire_on_commit, **kwargs)
