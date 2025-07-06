from injector import inject
from fastapi import APIRouter, Request
from common.enums import AppEndpoints
from ..services.scraper_service import ScraperService


class ScraperController:
    @inject
    def __init__(self, scraper_service: ScraperService) -> None:
        self._scraper_service = scraper_service
        self._router = APIRouter(
            prefix=AppEndpoints.SCRAPER.value, tags=["Scraper"]
        )
        self._register_routes()

    def _register_routes(self):
        @self._router.post("")
        async def get_url_image(req: Request):
            body = await req.json()
            query = body.get("query")
            source = body.get("source")
            result = self._scraper_service.get_image_url(
                {"query": query, "source": source}
            )
            return {"urls": result}

    def get_router(self) -> APIRouter:
        return self._router
