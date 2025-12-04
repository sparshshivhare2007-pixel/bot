from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URI)
db = client["rishu_bot"]
users = db["users"]
