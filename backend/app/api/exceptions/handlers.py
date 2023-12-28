from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Request, status

from app.api.exceptions import AppException, AggregateException, BadRequestFieldException, add_missing_punctuation


def exception_handler(_: Request, __: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            'errors': [
                {
                    'code': AppException.CODE,
                    'msg': AppException.DEFAULT_MESSAGE
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
    formatted_errors = []
    for error in e.errors():
        loc, code, msg = error['loc'], error['type'], error['msg']
        path_list = loc[1:]
        field_path = '.'.join(map(str, path_list))
        msg = add_missing_punctuation(message=msg)
        formatted_errors.append({
            'field': field_path,
            'code': code,
            'message': str(msg).capitalize()
        })

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({
            'errors': formatted_errors
        })
    )
