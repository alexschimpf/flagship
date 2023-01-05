import os
import ujson
import logging
import logging.config
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from app.api.exceptions.handlers import EXCEPTION_HANDLERS
from app.api.schemas import ErrorResponseModel


class Bootstrap:

    def run(self) -> FastAPI:
        self._init_logger()
        self._init_services()

        app = self._build_app()
        self._register_routes(app=app)
        self._add_cors_middleware(app=app)
        self._set_route_operation_ids(app=app)

        return app

    @staticmethod
    def _init_logger() -> None:
        config_file_path = os.path.join(os.path.dirname(__file__), '../config/logger.json')
        with open(config_file_path, 'r') as f:
            logger_config = ujson.loads(f.read())
            logging.config.dictConfig(config=logger_config)

    @staticmethod
    def _init_services() -> None:
        pass

    @classmethod
    def _build_app(cls) -> FastAPI:
        return FastAPI(
            title='Flagship API',
            version='1.0',
            responses={
                status_code: {'model': ErrorResponseModel}
                for status_code in (400, 401, 403, 404, 500)
            },
            exception_handlers=EXCEPTION_HANDLERS,
            swagger_ui_parameters={'defaultModelsExpandDepth': -1}
        )

    @staticmethod
    def _register_routes(app: FastAPI) -> None:
        from app import api
        app.include_router(api.router)

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


