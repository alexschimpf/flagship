from typing import TYPE_CHECKING, Any

import ujson
from redis import BusyLoadingError, ConnectionError, TimeoutError
from redis.cluster import RedisCluster
from redis.retry import Retry
from redis.backoff import ExponentialBackoff

from app.config import Config


class RedisService:

    if TYPE_CHECKING:
        _client: RedisCluster[str]
    else:
        _client: RedisCluster

    @classmethod
    def init(cls) -> None:
        cls._client = RedisCluster.from_url(
            url=Config.REDIS_CONN_STR,
            decode_responses=True,
            require_full_coverage=True,
            retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
            retry=Retry(ExponentialBackoff(), 3)
        )

    @classmethod
    def get_project_data(cls, project_id: int) -> tuple[Any, Any, Any]:
        pipeline = cls._client.pipeline()
        pipeline.hgetall(f'feature-flags:{project_id}')
        pipeline.hgetall(f'context-fields:{project_id}')
        pipeline.smembers(f'private-keys:{project_id}')
        feature_flags, context_fields, private_keys = pipeline.execute()

        for name, conditions in feature_flags.items():
            feature_flags[name] = ujson.loads(conditions)

        # TODO: Types?
        return feature_flags, context_fields, private_keys
