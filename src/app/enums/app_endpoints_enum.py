from enum import Enum


class AppEndpoints(Enum):
    HEALTH = "/health"
    FILE = "/files"
    UPLOAD = "/uploads"
    LANGUAGE = "/language"
    WORD = "/words"
