from pymongo import MongoClient
import config

# -------------------- DATABASE CONNECTION --------------------
mongo_client = MongoClient(config.MONGO_URL)

# Chatbot ke liye alag DB
chatbot_db = mongo_client["ChatBotDb"]

# Collections
users_col = chatbot_db["users"]
chats_col = chatbot_db["chats"]
couples_col = chatbot_db["couples"]

# Module imports
from .users import *
from .chats import *
from .couples import *
