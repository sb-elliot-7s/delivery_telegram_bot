from pydantic import BaseModel, Field, ConfigDict
from .obj_id import PyObjectId


class CreateDishSchema(BaseModel):
    name: str
    description: str
    photo: str
    price: str


class DishSchema(CreateDishSchema):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: PyObjectId = Field(alias='_id')


class DishResultSchema(BaseModel):
    dish: DishSchema | None
    message: str
    status_code: int
