import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["economy_bot"]
users = db["users"]

# Get or create user
def get_user(user_id):
    user = users.find_one({"user_id": user_id})
    if not user:
        users.insert_one({"user_id": user_id, "balance": 0})
        user = users.find_one({"user_id": user_id})
    return user

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

    # Inline URL buttons
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
    user_id = update.effective_user.id
    user = get_user(user_id)

    earn = 100
    new_balance = user["balance"] + earn
    users.update_one({"user_id": user_id}, {"$set": {"balance": new_balance}})

    await update.message.reply_text(
        f"🛠 You worked and earned {earn} coins!\n💰 New Balance: {new_balance}"
    )

# ---------------- /daily ----------------
async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    now = datetime.utcnow()

    if "last_daily" in user:
        last = user["last_daily"]
        if now - last < timedelta(hours=24):
            remaining = timedelta(hours=24) - (now - last)
            hours = remaining.seconds // 3600
            mins = (remaining.seconds % 3600) // 60
            return await update.message.reply_text(
                f"⏳ Already claimed!\nNext claim: **{hours}h {mins}m**"
            )

    reward = 500
    new_balance = user["balance"] + reward
    users.update_one({"user_id": user_id}, {"$set": {"balance": new_balance, "last_daily": now}})

    await update.message.reply_text(
        f"🎁 Daily Reward Claimed!\nEarned: {reward} coins\n💰 New Balance: {new_balance}"
    )

# ---------------- Polling Setup ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("work", work))
app.add_handler(CommandHandler("daily", daily))

if __name__ == "__main__":
    app.run_polling()
