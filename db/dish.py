from dataclasses import dataclass

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection


@dataclass
class Dish:
    collection: AsyncIOMotorCollection

    async def save_dish(self, dish_document: dict):
        await self.collection.insert_one(document=dish_document)

    async def delete_dish(self, dish_id: str):
        return (await self.collection.delete_one(filter={'_id': ObjectId(dish_id)})).deleted_count
