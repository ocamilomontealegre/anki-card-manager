from typing import Any
from asyncio import run
from injector import Injector
from common.mq.celery import celery_app
from modules.word.models.interfaces.find_all_params import FindAllParams
from ..services.anki_service import AnkiService


@celery_app.task(name="process_anki_cards")
def process_anki_cards(filters: Any) -> None:
    from app.app_module import AppModule

    container = Injector([AppModule()])
    anki_service = container.get(AnkiService)

    filters = FindAllParams(**filters)
    run(anki_service.create_cards(filters=filters))
