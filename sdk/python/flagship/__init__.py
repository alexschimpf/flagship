import json
import hmac
import hashlib
import requests
from typing import Any


class Flagship:

    def __init__(self, host: str, project_id: int, user_key: str, private_key: str, port: int = 443):
        """
        :param host: host name of Flagship API
        :param project_id:
        :param private_key: the secret key assigned to the project
        :param user_key: the user's unique key
        :param port: port of Flagship API
        """

        self._host = host
        self._scheme = 'https' if port == 443 else 'http'
        self._port = port
        self._project_id = project_id
        self._user_key = user_key
        self._private_key = private_key

        self._enabled_feature_flags: set[str] = set()

    def load(self, context: dict[str, Any], timeout: int = 60) -> set[str]:
        """
        Loads all of the enabled feature flags for a user, given some context

        :param context: dict
        :param timeout: request timeout (in seconds)
        :return: set of feature flags
        """

        signature = self.generate_signature()
        post_data = json.dumps(dict(context=context))
        headers = {
            'Signature': signature,
            'Content-Type': 'application/json'
        }
        api_url = f'{self._scheme}://{self._host}:{self._port}/feature_flags'
        params: dict[str, Any] = {
            'project_id': self._project_id,
            'user_key': self._user_key
        }
        response = requests.post(
            url=api_url,
            params=params,
            data=post_data,
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        response_json = response.json()
        self._enabled_feature_flags = set(response_json['feature_flags'] or ())
        return self._enabled_feature_flags

    def is_feature_flag_enabled(self, name: str) -> bool:
        """
        Determines if a feature flag is enabled, given some context.
        This assumes that load() has been called prior.

        :param name: name of the feature_flag
        :return: bool
        """

        return name in self._enabled_feature_flags

    def get_enabled_feature_flags(self) -> set[str]:
        """
        Returns all enabled feature flags, given some context.
        This assumes that load() has been called prior.

        :return: set of names of all enabled feature flags
        """

        return self._enabled_feature_flags

    def generate_signature(self) -> str:
        """
        Generates an HMAC signature based on the project's secret key and the user's key.
        This should be sent along with all requests to the Flagship API.

        :return: str
        """
        return hmac.new(
            self._private_key.encode(),
            self._user_key.encode(),
            hashlib.sha256
        ).hexdigest()
