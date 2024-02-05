from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.exceptions.exceptions import AppException, AggregateException, BadRequestFieldException, \
    UnauthenticatedException
from app.services.strings.service import StringsService


def exception_handler(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            'errors': [
                {
                    'code': AppException.CODE,
                    'msg': StringsService.get(key=AppException.CODE)
                }
            ]
        }
    )


def app_exception_handler(_: Request, e: AppException) -> JSONResponse:
    errors = []
    exceptions = e.exceptions if isinstance(e, AggregateException) else [e]
    for exc in exceptions:
        if isinstance(exc, BadRequestFieldException):
            errors.append({
                'field': exc.field,
                'code': exc.CODE,
                'message': str(exc)
            })
        else:
            errors.append({
                'code': exc.CODE,
                'message': str(exc)
            })

    return JSONResponse(
        status_code=e.STATUS,
        content={
            'errors': errors
        }
    )


def request_validation_exception_handler(_: Request, e: RequestValidationError) -> JSONResponse:
    # TODO: Handle i18n
    formatted_errors = []
    for error in e.errors():
        error_code, message = error['type'], error['msg']
        field = error['loc'][1]
        message = _make_user_friendly(error_code=error_code, field=field, message=message)
        formatted_errors.append({
            'field': field,
            'code': error_code.upper(),
            'message': message
        })

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({
            'errors': formatted_errors
        })
    )


def _make_user_friendly(error_code: str, field: str, message: str) -> str:
    if message and message[-1] not in ('.', '?', '!'):
        message += '.'

    if error_code in ('string_too_long', 'string_too_short'):
        message = message.replace('String', field)

    return message.capitalize()
