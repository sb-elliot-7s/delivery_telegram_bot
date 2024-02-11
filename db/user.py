from contextlib import suppress
from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError


@dataclass
class UserDB:
    collection: AsyncIOMotorCollection

    async def save_user(self, user_document: dict):
        with suppress(DuplicateKeyError):
            await self.collection.insert_one(document=user_document)
