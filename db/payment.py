from dataclasses import dataclass

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from schemas.payment import PaymentSchema, CreateSuccessfulPaymentSchema
from datetime import datetime


@dataclass
class Payment:
    collection: AsyncIOMotorCollection

    async def save_payment(self, payment_data: CreateSuccessfulPaymentSchema):
        await self.collection.insert_one(document=payment_data.model_dump())

    async def get_payment(self, payment_id: str):
        payment_result = await self.collection.find_one(filter={'_id': ObjectId(payment_id)})
        if payment_result:
            return PaymentSchema(**payment_result)
        return None

    async def get_payments(self, skip: int = 0, limit: int | None = None):
        return [payment async for payment in self.collection.find().limit(limit=limit).skip(skip=skip)]
