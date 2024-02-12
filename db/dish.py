from dataclasses import dataclass

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from schemas.dish import DishSchema, DishResultSchema


@dataclass
class Dish:
    collection: AsyncIOMotorCollection

    async def save_dish(self, dish_document: dict):
        await self.collection.insert_one(document=dish_document)

    async def delete_dish(self, dish_id: str):
        return (await self.collection.delete_one(filter={'_id': ObjectId(dish_id)})).deleted_count

    async def get_dishes(self, skip: int = 0, limit: int = 0):
        return [DishSchema(**dish) async for dish in self.collection.find().limit(limit=limit).skip(skip=skip)]

    async def get_dish(self, dish_id: str):
        document = await self.collection.find_one(filter={'_id': ObjectId(dish_id)})
        if document is None:
            return DishResultSchema(message='Dish not found', dish=None, status_code=404)
        return DishResultSchema(message='OK', dish=DishSchema(**document), status_code=200)
