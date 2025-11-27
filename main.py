import logging
from pymongo import MongoClient
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    ContextTypes
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ============================
#  MONGODB CONNECTION
# ============================
MONGO_URL = "YOUR_MONGO_URL"
client = MongoClient(MONGO_URL)
db = client["economy"]
users = db["users"]

# ============================
#  START COMMAND
# ============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    name = update.effective_user.first_name

    if not users.find_one({"user_id": uid}):
        users.insert_one({"user_id": uid, "balance": 1000, "killed": False})

    await update.message.reply_text(
        f"👋 Hello {name}!\nYour account is ready with 1000 coins."
    )

# ============================
#  OPEN & CLOSE
# ============================
game_open = True

async def open_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_open
    game_open = True
    await update.message.reply_text("✔️ Game is now OPEN!")

async def close_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_open
    game_open = False
    await update.message.reply_text("❌ Game is now CLOSED!")

# ============================
#  BALANCE
# ============================
async def bal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        t = users.find_one({"user_id": target.id})
        bal = t["balance"] if t else 0

        name = f"@{target.username}" if target.username else target.first_name
        return await update.message.reply_text(f"💰 {name}'s Balance: {bal}")

    uid = update.effective_user.id
    u = users.find_one({"user_id": uid})
    bal = u["balance"] if u else 0
    await update.message.reply_text(f"💰 Your Balance: {bal}")

# ============================
#  TOP RICHEST
# ============================
async def toprich(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = users.find().sort("balance", -1).limit(10)
    msg = "🏆 **Top 10 Richest Users:**\n\n"

    for i, u in enumerate(data, start=1):
        user_id = u["user_id"]
        bal = u["balance"]

        try:
            user_obj = await context.bot.get_chat(user_id)
            name = f"@{user_obj.username}" if user_obj.username else (user_obj.first_name or "Unknown")
        except:
            name = "Unknown"

        msg += f"{i}. {name}: ${bal}\n"

    msg += "\nNote: Use username for profile click"

    await update.message.reply_text(msg, parse_mode="Markdown")

# ============================
#  TOP KILLERS
# ============================
async def topkill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = users.find({"killed": True}).limit(10)

    msg = "💀 **Top Killed Users:**\n\n"

    for i, u in enumerate(data, start=1):
        user_id = u["user_id"]

        try:
            user_obj = await context.bot.get_chat(user_id)
            name = f"@{user_obj.username}" if user_obj.username else user_obj.first_name
        except:
            name = "Unknown"

        msg += f"{i}. {name}\n"

    await update.message.reply_text(msg, parse_mode="Markdown")

# ============================
#  KILL COMMAND
# ============================
async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Kisi ko kill karne ke liye reply karo!")

    killer = update.effective_user
    target = update.message.reply_to_message.from_user

    if killer.id == target.id:
        return await update.message.reply_text("❌ Khud ko thodi kill karega!")

    users.update_one(
        {"user_id": target.id},
        {"$set": {"balance": 0, "killed": True}},
        upsert=True
    )

    name = f"@{target.username}" if target.username else target.first_name

    await update.message.reply_text(
        f"⚔️ {name} **has been KILLED!**\n💀 Balance reset to **0**"
    )

# ============================
#  REVIVE COMMAND
# ============================
async def revive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply karke revive karo!")

    reviver = update.effective_user
    target = update.message.reply_to_message.from_user

    r = users.find_one({"user_id": reviver.id})
    if not r or r["balance"] < 200:
        return await update.message.reply_text("❌ Revive ke liye 200 coins chahiye!")

    t = users.find_one({"user_id": target.id})
    if not t or not t.get("killed"):
        return await update.message.reply_text("❌ Ye banda killed hi nahi hai!")

    users.update_one({"user_id": reviver.id}, {"$inc": {"balance": -200}})
    users.update_one({"user_id": target.id}, {"$set": {"killed": False}})

    name = f"@{target.username}" if target.username else target.first_name

    await update.message.reply_text(
        f"❤️ {name} **revived successfully!**\n💸 Cost: 200 coins"
    )

# ============================
#  MAIN APP
# ============================
async def main():
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("open", open_cmd))
    app.add_handler(CommandHandler("close", close_cmd))
    app.add_handler(CommandHandler("bal", bal))
    app.add_handler(CommandHandler("toprich", toprich))
    app.add_handler(CommandHandler("topkill", topkill))
    app.add_handler(CommandHandler("kill", kill))
    app.add_handler(CommandHandler("revive", revive))

    print("BOT STARTED WITH POLLING...")
    await app.run_polling()

import asyncio
asyncio.run(main())
