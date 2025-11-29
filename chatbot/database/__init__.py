from pymongo import MongoClient
import config  # Make sure you have config.py with MONGO_URL

mongo = MongoClient(config.MONGO_URL)
db = mongo.ChatDb  # Chatbot-specific database

chatsdb = db["chatsdb"]
usersdb = db["users"]
