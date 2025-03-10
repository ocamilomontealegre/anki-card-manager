from uuid import uuid4
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func
from common.database.entities.base_entity import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    language_id = Column(int, unique=False, nullable=False)
    word = Column(String(256), unique=False, nullable=False)
    definition = Column(String(256), unique=False, nullable=False)
    sentence = Column(String(256), unique=False, nullable=False)
    phonetics = Column(String(256), unique=False, nullable=False)
    sentence_audio = Column(String(256), unique=False, nullable=False)
    partial_sentence = Column(String(256), unique=False, nullable=False)
    singular = Column(String(256), unique=False, nullable=False)
    singular_audio = Column(String(256), unique=False, nullable=False)
    plural = Column(String(256), unique=False, nullable=True)
    plural_audio = Column(String(256), unique=False, nullable=True)
    synonyms = Column(String(256), unique=False, nullable=True)
    image = Column(String(256), unique=False, nullable=False)
    image_2 = Column(String(256), unique=False, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Word(id={self.id}, word={self.word})>"
