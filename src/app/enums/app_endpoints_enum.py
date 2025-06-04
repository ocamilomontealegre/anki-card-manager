from enum import Enum


class AppEndpoints(Enum):
    HEALTH = "/health"
    FILE = "/files"
    UPLOAD = "/uploads"
    LANGUAGE = "/languages"
    WORD = "/words"
    SCRAPER = "/scrapers"
    ANKI = "/anki"
    TASK = "/task"
