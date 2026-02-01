from asyncio import run

from injector import Injector

from common.mq.celery import celery_app

from ..services.language_service import LanguageService


@celery_app.task(name="process_csv_task")
def process_csv_task(file_path: str) -> None:
    from app.app_module import AppModule

    container = Injector([AppModule()])
    language_service = container.get(LanguageService)

    run(language_service.process_csv(file_name=file_path))
