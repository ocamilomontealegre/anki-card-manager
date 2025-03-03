from fastapi import APIRouter
from injector import Injector
from health.controllers.health_controller import HealthController
from modules.upload.controllers.upload_controller import UploadController
from modules.language.controllers.language_controller import LanguageController
from app.enums.app_endpoints_enum import AppEndpoints


class AppRouter:
    def __init__(self, injector: Injector):
        self.__router = APIRouter()
        self.__injector = injector
        self.__register_routes()

    def __register_routes(self):
        health_controller = self.__injector.get(HealthController)
        upload_controller = self.__injector.get(UploadController)
        language_controller = self.__injector.get(LanguageController)

        self.__router.include_router(
            health_controller.get_router(),
            prefix=AppEndpoints.HEALTH.value
        )

        self.__router.include_router(
            upload_controller.get_router(),
            prefix=AppEndpoints.UPLOAD.value
        )

        self.__router.include_router(
            language_controller.get_router(),
            prefix=AppEndpoints.LANGUAGE.value
        )

    def get_router(self) -> APIRouter:
        return self.__router
