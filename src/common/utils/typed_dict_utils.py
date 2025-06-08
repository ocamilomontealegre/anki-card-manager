from typing import Type, TypedDict
from pydantic import BaseModel


class TypedDictUtils:
    @staticmethod
    def from_pydantic(model: Type[BaseModel]) -> type:
        annotations = {
            name: field.annotation
            for name, field in model.model_fields.items()
        }
        return type(f"{model.__name__}TypedDict", (TypedDict,), {'__annotations__': annotations})
