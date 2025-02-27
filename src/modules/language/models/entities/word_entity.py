from uuid import uuid4
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func
from common.database.entities.base_entity import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    definition = Column(String(256), unique=False, nullable=False)
    created_at = Column(DateTime, de}
    
    )