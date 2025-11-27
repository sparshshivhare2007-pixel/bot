import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["economy_bot"]
users = db["users"]
groups = db["groups"]  # to store group economy status

# ----------------- Helper Functions -----------------
def is_killed(user_id):
    user = users.find_one({"user_id": user_id})
    return user.get("killed", False)

def get_user(user_id):
    user = users.find_one({"user_id": user_id})
    if not user:
        users.insert_one({
            "user_id": user_id,
            "balance": 0,
            "kills": 0,
            "killed": False
        })
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

# ----------------- /balance -----------------
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_obj = update.message.reply_to_message.from_user
    else:
        user_obj = update.effective_user

    user_id = user_obj.id

    db_user = users.find_one({"user_id": user_id})
    if not db_user:
        users.insert_one({
            "user_id": user_id,
            "username": user_obj.username,
            "name": user_obj.full_name,
            "balance": 0,
            "kills": 0,
            "killed": False
        })
        db_user = users.find_one({"user_id": user_id})

    rank_pipeline = [
        {"$sort": {"balance": -1}},
        {"$group": {"_id": None, "users": {"$push": "$user_id"}}}
    ]
    rank_data = list(users.aggregate(rank_pipeline))
    rank = rank_data[0]["users"].index(user_id) + 1 if rank_data else 1

    status = "☠️ Dead" if db_user.get("killed") else "Alive"
    display_name = f"@{db_user.get('username')}" if db_user.get("username") else db_user.get("name")

    message = (
        f"👤 Name: {display_name}\n"
        f"💰 Total Balance: {db_user.get('balance')}\n"
        f"🏆 Global Rank: #{rank}\n"
        f"❤️ Status: {status}\n"
        f"⚔️ Kills: {db_user.get('kills')}"
    )

    await update.message.reply_text(message)

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
    users.update_one({"user_id": user["user_id"]},
                     {"$set": {"balance": new_balance, "last_daily": now}})
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

    if target["balance"] <= 0:
        return await update.message.reply_text("❌ Target has no coins!")

    amount = random.randint(1, min(1000, target["balance"]))
    users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": amount}})
    users.update_one({"user_id": target_user_id}, {"$inc": {"balance": -amount}})
    await update.message.reply_text(f"💸 You robbed {amount} coins!")

# ----------------- /protect -----------------
async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group_open(update.effective_chat.id):
        return await update.message.reply_text("❌ Economy commands are closed in this group!")
    if random.choice([True, False]):
        await update.message.reply_text("🛡 You are protected from the next robbery!")
    else:
        await update.message.reply_text("⚠️ Protection failed! Try again.")

# ----------------- /toprich -----------------
async def toprich(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_users = users.find().sort("balance", -1).limit(10)
    msg = "🏆 Top 10 Richest Users:\n\n"

    for idx, user in enumerate(top_users, start=1):
        try:
            chat = await context.bot.get_chat(user["user_id"])
            username = f"@{chat.username}" if chat.username else chat.first_name
        except:
            username = "Unknown"

        msg += f"{idx}. {username}: ${user['balance']}\n"

    msg += "\nNote: Use username for clickable profile."
    await update.message.reply_text(msg)

# ----------------- /topkill -----------------
async def topkill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_users = users.find().sort("kills", -1).limit(10)
    msg = "⚔️ Top 10 Killers:\n\n"

    for idx, user in enumerate(top_users, start=1):
        try:
            chat = await context.bot.get_chat(user["user_id"])
            username = f"@{chat.username}" if chat.username else chat.first_name
        except:
            username = "Unknown"

        msg += f"{idx}. {username}: {user.get('kills', 0)} kills\n"

    await update.message.reply_text(msg)

# ----------------- /kill -----------------
async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group_open(update.effective_chat.id):
        return await update.message.reply_text("❌ Economy commands are closed in this group!")

    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to the user you want to kill.")

    killer_id = update.effective_user.id
    target_id = update.message.reply_to_message.from_user.id

    if killer_id == target_id:
        return await update.message.reply_text("❌ You cannot kill yourself!")

    target = get_user(target_id)

    if target.get("killed", False):
        return await update.message.reply_text("❌ This user is already killed. Revive them!")

    users.update_one({"user_id": killer_id}, {"$inc": {"kills": 1}})
    users.update_one({"user_id": target_id}, {"$set": {"balance": 0, "killed": True}})

    await update.message.reply_text(
        f"⚔️ {update.effective_user.first_name} killed {update.message.reply_to_message.from_user.first_name}!\n"
        f"💀 Balance is now 0 and status set to killed."
    )

# ----------------- /revive -----------------
async def revive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to the user you want to revive.")

    target_id = update.message.reply_to_message.from_user.id
    target = get_user(target_id)

    if not target.get("killed", False):
        return await update.message.reply_text("❌ This user is not killed!")

    if target["balance"] < 200:
        return await update.message.reply_text("❌ User does not have 200 coins to revive!")

    new_balance = target["balance"] - 200
    users.update_one({"user_id": target_id}, {"$set": {"balance": new_balance, "killed": False}})

    await update.message.reply_text(
        f"❤️ {update.message.reply_to_message.from_user.first_name} has been revived!\n"
        f"💰 200 coins deducted\n📌 New Balance: {new_balance}"
    )

# ----------------- /close -----------------
async def close(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        set_group_status(update.effective_chat.id, False)
        await update.message.reply_text("❌ Economy commands are now CLOSED in this group!")

# ----------------- /open -----------------
async def open_economy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        set_group_status(update.effective_chat.id, True)
        await update.message.reply_text("✅ Economy commands are now OPEN in this group!")

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
app.add_handler(CommandHandler("kill", kill))
app.add_handler(CommandHandler("revive", revive))

if __name__ == "__main__":
    app.run_polling()
