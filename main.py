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
    update_user(user_id, {"balance": new_balance, "last_daily": now})

    await update.message.reply_text(
        f"🎁 Daily Reward Claimed!\nEarned: {reward} coins\n💰 New Balance: {new_balance}"
    )

# ---------------- /rob ----------------
async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to someone to rob them!")

    robber_id = update.effective_user.id
    target_id = update.message.reply_to_message.from_user.id

    if robber_id == target_id:
        return await update.message.reply_text("❌ You cannot rob yourself!")

    robber = get_user(robber_id)
    target = get_user(target_id)

    if target.get("protection") and target["protection"] > datetime.utcnow():
        return await update.message.reply_text("🛡 Target is protected!")

    if target["balance"] <= 0:
        return await update.message.reply_text("❌ Target has no coins!")

    amount = randint(1, min(1000, target["balance"]))
    update_user(robber_id, {"balance": robber["balance"] + amount})
    update_user(target_id, {"balance": target["balance"] - amount})

    await update.message.reply_text(
        f"💰 You robbed {amount} coins from {update.message.reply_to_message.from_user.first_name}!"
    )

# ---------------- /protect ----------------
async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    args = context.args

    if not args or args[0] not in ["1d", "2d"]:
        return await update.message.reply_text("Usage: /protect 1d or /protect 2d")

    days = int(args[0][0])
    cost = 500 * days
    if user["balance"] < cost:
        return await update.message.reply_text(f"❌ You need {cost} coins!")

    new_protection = datetime.utcnow() + timedelta(days=days)
    update_user(user_id, {"balance": user["balance"] - cost, "protection": new_protection})

    await update.message.reply_text(
        f"🛡 Protection active for {days} day(s)!\n💰 Remaining Balance: {user['balance'] - cost}"
    )

# ---------------- Polling Setup ----------------
app = ApplicationBuilder().token(TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("work", work))
app.add_handler(CommandHandler("daily", daily))
app.add_handler(CommandHandler("rob", rob))
app.add_handler(CommandHandler("protect", protect))

# Run bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
