import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["economy_bot"]
users = db["users"]

def get_user(user_id):
    user = users.find_one({"user_id": user_id})
    if not user:
        users.insert_one({"user_id": user_id, "balance": 0})
        user = users.find_one({"user_id": user_id})
    return user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    await update.message.reply_text(
        f"👋 Welcome {update.effective_user.first_name}!\n"
        f"Your balance is: 💰 {user['balance']} coins"
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    await update.message.reply_text(f"💰 Your balance: {user['balance']} coins")

async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    earn = 100
    new_balance = user["balance"] + earn
    users.update_one({"user_id": user["user_id"]}, {"$set": {"balance": new_balance}})
    await update.message.reply_text(f"🛠 You worked and earned {earn} coins!\nNew Balance: {new_balance}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("work", work))

app.run_polling()

