from motor.motor_asyncio import AsyncIOMotorClient
import config

client = AsyncIOMotorClient(config.MONGO_DB_URL)
db = client["economy_bot"]

users = db["users"]

async def get_user(user_id):
    user = await users.find_one({"_id": user_id})
    if not user:
        user = {"_id": user_id, "wallet": 0, "bank": 0, "daily": 0}
        await users.insert_one(user)
    return user

async def update_user(user_id, data):
    await users.update_one({"_id": user_id}, {"$set": data})
