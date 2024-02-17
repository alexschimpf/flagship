import os
from typing import Final

import ujson

from app.config import Config


class StringsService:
    DEFAULT_LOCALE: str
    LOOKUP: Final[dict[str, dict[str, str]]] = {}

    @classmethod
    def init(cls, default_locale: str) -> None:
        file_path = os.path.join(os.path.dirname(__file__), '../../../config/strings.json')
        with open(file_path) as file:
            cls.LOOKUP.update(ujson.loads(file.read()))

        cls.DEFAULT_LOCALE = default_locale

    @classmethod
    def get(cls, key: str, fallback_locale: str = 'en-us') -> str:
        key = key.upper()
        locale = Config.DEFAULT_LOCALE.lower()
        if locale in cls.LOOKUP[key]:
            if locale in cls.LOOKUP[key]:
                return cls.LOOKUP[key][locale]
            if fallback_locale in cls.LOOKUP[key]:
                return cls.LOOKUP[key][fallback_locale]

        raise Exception(f'No translation found for key ({key}) and locale ({locale})')
