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
groups = db["groups"]  # to store group economy status

# ----------------- Helper Functions -----------------
def get_user(user_id):
    user = users.find_one({"user_id": user_id})
    if not user:
        users.insert_one({"user_id": user_id, "balance": 0, "kills": 0})
        user = users.find_one({"user_id": user_id})
    return user

def is_group_open(chat_id):
    group = groups.find_one({"chat_id": chat_id})
    return group.get("open", True) if group else True

def set_group_status(chat_id, status: bool):
    groups.update_one({"chat_id": chat_id}, {"$set": {"open": status}}, upsert=True)

# ----------------- /start -----------------
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

# ----------------- /balance or /bal -----------------
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = update.effective_user.id
    user = get_user(user_id)
    await update.message.reply_text(f"💰 Balance: {user['balance']} coins")

# ----------------- /work -----------------
async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group_open(update.effective_chat.id):
        return await update.message.reply_text("❌ Economy commands are closed in this group!")

    user = get_user(update.effective_user.id)
    earn = 100
    new_balance = user["balance"] + earn
    users.update_one({"user_id": user["user_id"]}, {"$set": {"balance": new_balance}})
    await update.message.reply_text(f"🛠 You worked and earned {earn} coins!\n💰 New Balance: {new_balance}")

# ----------------- /daily -----------------
async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group_open(update.effective_chat.id):
        return await update.message.reply_text("❌ Economy commands are closed in this group!")

    user = get_user(update.effective_user.id)
    now = datetime.utcnow()

    if "last_daily" in user:
        last = user["last_daily"]
        if now - last < timedelta(hours=24):
            remaining = timedelta(hours=24) - (now - last)
            hours = remaining.seconds // 3600
            mins = (remaining.seconds % 3600) // 60
            return await update.message.reply_text(f"⏳ Already claimed!\nNext claim: {hours}h {mins}m")

    reward = 500
    new_balance = user["balance"] + reward
    users.update_one({"user_id": user["user_id"]}, {"$set": {"balance": new_balance, "last_daily": now}})
    await update.message.reply_text(f"🎁 Daily Reward Claimed!\nEarned: {reward} coins\n💰 New Balance: {new_balance}")

# ----------------- /rob -----------------
async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group_open(update.effective_chat.id):
        return await update.message.reply_text("❌ Economy commands are closed in this group!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to the user you want to rob.")
    
    user = get_user(update.effective_user.id)
    target_user_id = update.message.reply_to_message.from_user.id
    target = get_user(target_user_id)

    import random
    amount = random.randint(1, min(1000, target["balance"]))
    if target["balance"] < amount:
        return await update.message.reply_text("❌ Target has no coins to rob!")
    
    users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": amount}})
    users.update_one({"user_id": target_user_id}, {"$inc": {"balance": -amount}})
    await update.message.reply_text(f"💸 You robbed {amount} coins from {update.message.reply_to_message.from_user.first_name}!")

# ----------------- /protect -----------------
async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group_open(update.effective_chat.id):
        return await update.message.reply_text("❌ Economy commands are closed in this group!")
    import random
    success = random.choice([True, False])
    user = get_user(update.effective_user.id)
    if success:
        await update.message.reply_text("🛡 You are protected from the next robbery!")
    else:
        await update.message.reply_text("⚠️ Protection failed! Try again.")

# ----------------- /toprich -----------------
async def toprich(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_users = users.find().sort("balance", -1).limit(10)
    msg = "🏆 Top 10 Richest Users:\n"

    for idx, user in enumerate(top_users, start=1):
        try:
            chat = await context.bot.get_chat(user["user_id"])
            name = chat.first_name or "Unknown"
            username = f"@{chat.username}" if chat.username else name
        except:
            name = "Unknown"
            username = "Unknown"

        msg += f"{idx}. {username}: ${user['balance']}\n"

    msg += "\nNote: Use username for making your profile clickable"
    await update.message.reply_text(msg)


# ----------------- /topkill -----------------
async def topkill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_users = users.find().sort("kills", -1).limit(10)
    msg = "⚔️ Top 10 Killers:\n"

    for idx, user in enumerate(top_users, start=1):
        try:
            chat = await context.bot.get_chat(user["user_id"])
            name = chat.first_name or "Unknown"
            username = f"@{chat.username}" if chat.username else name
        except:
            name = "Unknown"
            username = "Unknown"

        msg += f"{idx}. {username}: {user.get('kills', 0)}\n"

    await update.message.reply_text(msg)



# ----------------- /close -----------------
async def close(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        set_group_status(update.effective_chat.id, False)
        await update.message.reply_text("❌ Economy commands are now closed in this group!")

# ----------------- /open -----------------
async def open_economy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        set_group_status(update.effective_chat.id, True)
        await update.message.reply_text("✅ Economy commands are now open in this group!")

# ----------------- App Setup -----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("bal", balance))
app.add_handler(CommandHandler("work", work))
app.add_handler(CommandHandler("daily", daily))
app.add_handler(CommandHandler("rob", rob))
app.add_handler(CommandHandler("protect", protect))
app.add_handler(CommandHandler("toprich", toprich))
app.add_handler(CommandHandler("topkill", topkill))
app.add_handler(CommandHandler("close", close))
app.add_handler(CommandHandler("open", open_economy))

if __name__ == "__main__":
    app.run_polling()
