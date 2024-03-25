from typing import TypeVar

from fastapi import FastAPI

from application.main_lifespan import lifespan
from presentation import main_router

FastAPIInstance = TypeVar("FastAPIInstance", bound="FastAPI")


class ApiServer:
    """Сервер апи"""

    app_profile = FastAPI(lifespan=lifespan)
    app_profile.include_router(router=main_router)

    def __init__(self, app: FastAPI):
        self.__app = app

    def get_app(self) -> FastAPIInstance:
        return self.__app
