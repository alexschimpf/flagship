from typing import TYPE_CHECKING, Any

import ujson
from redis import BusyLoadingError, ConnectionError, TimeoutError
from redis.cluster import RedisCluster
from redis.retry import Retry
from redis.backoff import ExponentialBackoff

from app.api.routes.feature_flags.schemas import FeatureFlagCondition
from app.config import Config
from app.constants import ContextValueType


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
    def add_project_private_key(cls, project_id: int, encrypted_private_key: str) -> None:
        cls._client.sadd(f'private-keys:{{{project_id}}}', encrypted_private_key)

    @classmethod
    def remove_project_private_key(cls, project_id: int, encrypted_private_key: str) -> None:
        cls._client.srem(f'private-keys:{{{project_id}}}', encrypted_private_key)

    @classmethod
    def add_or_replace_feature_flag(
        cls,
        project_id: int,
        feature_flag_name: str,
        conditions: list[list[FeatureFlagCondition]],
        is_enabled: bool
    ) -> None:
        if is_enabled:
            conditions_str = ujson.dumps([
                [condition.model_dump() for condition in and_group]
                for and_group in conditions
            ])
            cls._client.hset(f'feature-flags:{{{project_id}}}', feature_flag_name, conditions_str)
        else:
            cls.remove_feature_flag(project_id=project_id, feature_flag_name=feature_flag_name)

    @classmethod
    def remove_feature_flag(cls, project_id: int, feature_flag_name: str) -> None:
        cls._client.hdel(f'feature-flags:{{{project_id}}}', feature_flag_name)

    @classmethod
    def add_or_replace_context_field(
        cls,
        project_id: int,
        context_field_key: str,
        context_value_type: ContextValueType
    ) -> None:
        cls._client.hset(f'context-fields:{{{project_id}}}', context_field_key, str(context_value_type))

    @classmethod
    def remove_context_field(cls, project_id: int, context_field_key: str) -> None:
        cls._client.hdel(f'context-fields:{{{project_id}}}', context_field_key)

    @classmethod
    def remove_project(cls, project_id: int) -> None:
        pipeline = cls._client.pipeline()
        pipeline.delete(f'private-keys:{{{project_id}}}')
        pipeline.delete(f'feature-flags:{{{project_id}}}')
        pipeline.delete(f'context-fields:{{{project_id}}}')
        pipeline.execute()
