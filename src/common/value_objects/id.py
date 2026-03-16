import ulid
from dataclasses import dataclass, Field

from src.common.value_objects.value_object import ValueObject


@dataclass(frozen=True)
class Id(ValueObject):
    value: str = Field(default_factory=lambda: ulid.new())


id = Id()
print(id)
