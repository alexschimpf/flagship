from typing import Any

from app.api.exceptions.exceptions import InvalidEnumDefException


def validate_enum_def(
    enum_def: dict[str, Any] | None
) -> None:
    if enum_def is None:
        return

    for key, value in enum_def.items() or {}:
        if (
            not isinstance(key, str) or
            type(value) not in (str, int, float) or
            key.strip() == '' or
            len(key) > 32 or
            (isinstance(value, str) and (value or '').strip() == '') or
            (isinstance(value, str) and len(value) > 128)
        ):
            raise InvalidEnumDefException(field='enum_def')
