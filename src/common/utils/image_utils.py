from typing import TypedDict
from pathlib import Path
from uuid import uuid4
from io import BytesIO
from aiohttp import ClientSession
from PIL import Image


class DownloadFromUrl(TypedDict):
    url: str
    word: str
    source: str


class ImageUtils:
    @staticmethod
    async def download_from_url(data: DownloadFromUrl) -> str:
        url = data["url"]
        word = data["word"]
        source = data["source"]

        extension = "gif" if "giphy" in url else "jpg"

        path = Path(source) / f"{word}__{uuid4().hex[:8]}.{extension}"

        async with ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                image_bytes = await response.read()

        image = Image.open(BytesIO(image_bytes))
        resize = image.resize((400, 300))
        resize.save(path)

        return str(path)
