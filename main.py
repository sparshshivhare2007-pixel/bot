import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
from random import randint

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["economy_bot"]
users = db["users"]
groups = db["groups"]  # For group economy status

# ----------------------
# Helper Functions
# ----------------------
def get_user(user_id):
    user = users.find_one({"user_id": user_id})
    if not user:
        users.insert_one({"user_id": user_id, "balance": 0})
        user = users.find_one({"user_id": user_id})
    return user

def update_user(user_id, data):
    users.update_one({"user_id": user_id}, {"$set": data})

def get_group_status(chat_id):
    group = groups.find_one({"group_id": chat_id})
    if not group:
        groups.insert_one({"group_id": chat_id, "economy_status": True})
        return True
    return group.get("economy_status", True)

def set_group_status(chat_id, status: bool):
    groups.update_one({"group_id": chat_id}, {"$set": {"economy_status": status}}, upsert=True)

# ---------------- /start ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    name = update.effective_user.first_name

    bot_title = "🔱 SPARSH ECONOMY BOT 🔱"
    custom_msg = (
        "✨ Welcome to the Economy World!\n"
        "🔥 Earn coins using work, daily & more!\n"
        "💼 Use buttons below to visit support."
    )

    keyboard = [
        [
            InlineKeyboardButton("💬 Support Group", url="https://t.me/mich_family_group"),
            InlineKeyboardButton("📢 Support Channel", url="https://t.me/mich_family_group")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"{bot_title}\n\n👋 Hello **{name}**!\n\n{custom_msg}\n\n💰 Your balance: {user['balance']} coins",
        reply_markup=reply_markup
    )

# ---------------- /balance ----------------
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    await update.message.reply_text(f"💰 Your current balance: {user['balance']} coins")

# ---------------- /work ----------------
async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not get_group_status(chat_id):
        return await update.message.reply_text("❌ Economy commands are disabled in this group!")

    user_id = update.effective_user.id
    user = get_user(user_id)

    earn = 100
    new_balance = user["balance"] + earn
    update_user(user_id, {"balance": new_balance})

    await update.message.reply_text(
        f"🛠 You worked and earned {earn} coins!\n💰 New Balance: {new_balance}"
    )

# ---------------- /daily ----------------
async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not get_group_status(chat_id):
        return await update.message.reply_text("❌ Economy commands are disabled in this group!")

    user_id = update.effective_user.id
    user = get_user(user_id)
    now = datetime.utcnow()

    if "last_daily" in user:
        last = user["last_daily"]
        if now - last
