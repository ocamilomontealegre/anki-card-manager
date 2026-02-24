from asyncio import run

from injector import Injector

from common.mq.celery import celery_app
from modules.word.models.interfaces.list_params import ListParams

from ..services.anki_service import AnkiService


@celery_app.task(name="process_anki_cards")
def process_anki_cards(params: ListParams) -> None:
    from app.app_module import AppModule

    container = Injector([AppModule()])
    anki_service = container.get(AnkiService)

    run(anki_service.create_cards(params=params))
