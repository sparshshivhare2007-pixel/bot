import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta

# Load .env file
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["economy_bot"]
users = db["users"]

# Fetch or create user
def get_user(user_id):
    user = users.find_one({"user_id": user_id})
    if not user:
        users.insert_one({"user_id": user_id, "balance": 0})
        user = users.find_one({"user_id": user_id})
    return user

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    await update.message.reply_text(
        f"👋 Welcome {update.effective_user.first_name}!\n"
        f"Your balance: 💰 {user['balance']} coins"
    )

# /balance command
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    await update.message.reply_text(
        f"💰 Your current balance: {user['balance']} coins"
    )

# /work command
async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    earn = 100
    new_balance = user["balance"] + earn

    users.update_one(
        {"user_id": user_id},
        {"$set": {"balance": new_balance}}
    )

    await update.message.reply_text(
        f"🛠 You worked and earned {earn} coins!\n"
        f"💰 New Balance: {new_balance}"
    )

# /daily command (24-hour cooldown)
async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    now = datetime.utcnow()

    # Check cooldown
    if "last_daily" in user:
        last = user["last_daily"]
        if now - last < timedelta(hours=24):
            remaining = timedelta(hours=24) - (now - last)
            hours = remaining.seconds // 3600
            mins = (remaining.seconds % 3600) // 60

            return await update.message.reply_text(
                f"⏳ You already claimed the daily reward!\n"
                f"Come back after **{hours}h {mins}m**."
            )

    reward = 500
    new_balance = user["balance"] + reward

    users.update_one(
        {"user_id": user_id},
        {"$set": {"balance": new_balance, "last_daily": now}}
    )

    await update.message.reply_text(
        f"🎁 Daily Reward Claimed!\n"
        f"You received **{reward} coins**.\n"
        f"💰 New Balance: {new_balance}"
    )

# Build the bot
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("work", work))
app.add_handler(CommandHandler("daily", daily))

# Run bot
app.run_polling()
