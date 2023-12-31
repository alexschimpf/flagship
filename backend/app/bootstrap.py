import logging
import logging.config
import os
from typing import Any

import fastapi.openapi.utils
import ujson
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from app.api import exceptions
from app.api.exceptions import handlers as exception_handlers
from app.api.routers import router
from app.api.schemas import ErrorResponseModel
from app.services.database.mysql.service import MySQLService


class Bootstrap:

    def run(self) -> FastAPI:
        self._init_logger()

        app = self._build_app()
        self._init_services()
        self._register_routes(app=app)
        self._override_openapi(app=app)
        self._add_cors_middleware(app=app)
        self._set_route_operation_ids(app=app)

        return app

    @staticmethod
    def _init_logger() -> None:
        config_file_path = os.path.join(os.path.dirname(__file__), '../config/logger.json')
        with open(config_file_path, 'r') as f:
            logger_config = ujson.loads(f.read())
            logging.config.dictConfig(config=logger_config)

    @classmethod
    def _build_app(cls) -> FastAPI:
        exceptions_handlers: dict[Any, Any] = {
            Exception: exception_handlers.exception_handler,
            exceptions.AppException: exception_handlers.app_exception_handler,
            RequestValidationError: exception_handlers.request_validation_exception_handler
        }
        return FastAPI(
            title='Flagship API',
            version='1.0',
            responses={
                400: {
                    'model': ErrorResponseModel
                }
            },
            exception_handlers=exceptions_handlers,
            swagger_ui_parameters={'defaultModelsExpandDepth': -1}
        )

    @staticmethod
    def _init_services() -> None:
        MySQLService.init()

    @staticmethod
    def _register_routes(app: FastAPI) -> None:
        app.include_router(router)

    @staticmethod
    def _override_openapi(app: FastAPI) -> None:
        def openapi() -> dict[str, Any]:
            openapi_schema = fastapi.openapi.utils.get_openapi(
                title=app.title,
                version=app.version,
                routes=app.routes
            )

            # Remove 422 response from schema
            for schema_path in openapi_schema['paths']:
                for method in openapi_schema['paths'][schema_path]:
                    openapi_schema['paths'][schema_path][method]['responses'].pop('422', None)

            return openapi_schema

        app.openapi = openapi  # type: ignore

    @staticmethod
    def _set_route_operation_ids(app: FastAPI) -> None:
        for route in app.routes:
            if isinstance(route, APIRoute):
                route.operation_id = route.name

    @staticmethod
    def _add_cors_middleware(app: FastAPI) -> None:
        # TODO: Make this configurable
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
