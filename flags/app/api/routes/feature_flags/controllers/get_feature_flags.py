from typing import Any, cast
import hmac
import hashlib
from cryptography.fernet import Fernet
import ujson

from app.config import Config
from app.services.database.redis.service import RedisService
from app.api.routes.feature_flags.schemas import FeatureFlags
from app.api.exceptions.exceptions import UnauthorizedException
from app.api.routes.feature_flags.condition_checker import ConditionChecker


class GetFeatureFlagsController:

    def __init__(
        self,
        project_id: int,
        user_key: str,
        context: dict[str, Any],
        signature: str
    ):
        self.project_id = project_id
        self.user_key = user_key
        self.context = context
        self.signature = signature

    def handle_request(self) -> FeatureFlags:
        feature_flags, context_fields, encrypted_private_keys = \
            RedisService.get_project_data(project_id=self.project_id)
        self._validate(encrypted_private_keys=encrypted_private_keys)
        enabled_feature_flags = self._get_enabled_feature_flags(
            feature_flags=feature_flags, context_fields=context_fields)
        return FeatureFlags(
            items=enabled_feature_flags
        )

    def _validate(self, encrypted_private_keys: set[str]) -> None:
        for encrypted_private_key in encrypted_private_keys:
            f = Fernet(Config.SECRET_KEY.encode())
            private_key = f.decrypt(encrypted_private_key.encode()).decode()
            if self._is_signature_valid(private_key=private_key):
                return

        raise UnauthorizedException

    def _get_enabled_feature_flags(
        self,
        feature_flags: dict[str, list[list[dict[str, Any]]] | None],
        context_fields: dict[str, str]
    ) -> list[str]:
        enabled_feature_flags = []
        if feature_flags and context_fields:
            for feature_flag_name, conditions in feature_flags.items():
                if self._is_feature_flag_enabled(conditions=conditions, context_fields=context_fields):
                    enabled_feature_flags.append(feature_flag_name)

        return enabled_feature_flags

    def _is_feature_flag_enabled(
        self,
        conditions: list[list[dict[str, Any]]] | None,
        context_fields: dict[str, str]
    ) -> bool:
        if conditions in (None, []):
            return True

        for and_group in conditions or []:
            for condition in and_group:
                context_key = condition['context_key']
                context_value = self.context.get(context_key)
                context_value_type = int(context_fields[context_key])
                operator = condition['operator']
                value = condition['value']
                if not ConditionChecker.check(
                    context_value=context_value,
                    context_value_type=context_value_type,
                    operator=operator,
                    condition_value=value
                ):
                    # And group failed check
                    break
            else:
                # And group passed check
                return True

        return False

    def _is_signature_valid(self, private_key: str) -> bool:
        true_signature = hmac.new(
            private_key.encode(), self.user_key.encode(), hashlib.sha256).hexdigest()
        return self.signature == true_signature
