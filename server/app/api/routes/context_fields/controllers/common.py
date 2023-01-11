from typing import Any
from varname import nameof
import ujson

from app.api.routes.context_fields import schemas
from app.api import exceptions


def validate_enum_def(
    request: schemas.CreateContextField | schemas.UpdateContextField,
    errors: list[exceptions.AppException]
) -> None:
    if request.enum_def is None:
        return

    enum_def: dict[Any, Any]
    try:
        # TODO: Handle case of non-unique keys
        enum_def = ujson.loads(request.enum_def)
    except Exception:
        errors.append(exceptions.InvalidEnumDefException(field=nameof(request.enum_def)))
    else:
        for key, value in enum_def.items() or {}:
            if (
                not isinstance(key, str) or
                type(value) not in (str, int, float) or
                key.strip() == '' or
                len(key) > 32 or
                (isinstance(value, str) and (value or '').strip() == '') or
                (isinstance(value, str) and len(value) > 128)
            ):
                errors.append(exceptions.InvalidEnumDefException(field=nameof(request.enum_def)))
                break

        # Remove whitespace from JSON string
        request.enum_def = ujson.dumps(enum_def)
