from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from pydantic import PlainSerializer, AfterValidator, WithJsonSchema


class CreateDishSchema(BaseModel):
    name: str
    description: str
    photo: str
    price: str


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[
    str | ObjectId,
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]


class DishSchema(CreateDishSchema):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: PyObjectId = Field(alias='_id')


class DishResultSchema(BaseModel):
    dish: DishSchema | None
    message: str
    status_code: int
