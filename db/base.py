import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection

client = motor.motor_asyncio.AsyncIOMotorClient()

db = client.delivery

user_collection: AsyncIOMotorCollection = db.users
dish_collection: AsyncIOMotorCollection = db.dishes
