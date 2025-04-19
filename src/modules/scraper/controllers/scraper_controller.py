from injector import inject
from fastapi import APIRouter, Request
from ..services.scraper_service import ScraperService


class ScraperController:
    @inject
    def __init__(self, scraper_service: ScraperService) -> None:
        self.__scraper_service = scraper_service
        self.__router = APIRouter()
        self.__register_routes()

    def __register_routes(self):
        @self.__router.post("")
        async def get_url_image(req: Request):
            body = await req.json()
            query = body.get('query')
            result = await self.__scraper_service.get_image_url(query)
            return {"url": result}

    def get_router(self) -> APIRouter:
        return self.__router
