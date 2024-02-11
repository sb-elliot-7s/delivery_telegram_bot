from pydantic import BaseModel


class DishSchema(BaseModel):
    name: str
    description: str
    photo: str
    price: str
