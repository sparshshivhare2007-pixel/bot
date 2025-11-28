# main.py
import os
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ChatMemberHandler
)
from pymongo import MongoClient

# Helpers
from helpers import get_user, users, add_group_user

# Commands
from commands.start_command import start_command, button_handler

# Economy commands
from commands.economy_guide import economy_guide
from commands.transfer_balance import transfer_balance
from commands.claim import claim
from commands.own import own
from commands.crush import crush
from commands.love import love
from commands.slap import slap
from commands.items import items
from commands.item import item
from commands.give import give
from commands.daily import daily
from commands.rob import rob
from commands.protect import protect
from commands.toprich import toprich
from commands.topkill import topkill
from commands.kill import kill
from commands.revive import revive
from commands.open_economy import open_economy
from commands.close_economy import close_economy
from commands.punch import punch
from commands.hug import hug
from commands.couple import couple

# Load environment
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 0))
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB log system
client = MongoClient(MONGO_URI)
db = client["economy_bot"]
settings = db["settings"]

def get_log_chat_id():
    log_setting = settings.find_one({"_id": "log_chat"})
    return log_setting.get("chat_id") if log_setting else None

def is_owner(user_id):
    return user_id == OWNER_ID

async def send_log_message(bot: Bot, text: str, parse_mode='HTML'):
    target_id = get_log_chat_id() or OWNER_ID
    if target_id:
        try:
            await bot.send_message(chat_id=target_id, text=text, parse_mode=parse_mode)
        except Exception as e:
            print(f"❌ Error sending log: {e}")

# Track group users
async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat and update.effective_chat.type in ["group", "supergroup"]:
        user = update.effective_user
        if user:
            add_group_user(update.effective_chat.id, user.id, user.first_name)

# Balance command
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        user_id = target_user.id
        name = target_user.first_name
    else:
        user_id = update.effective_user.id
        name = update.effective_user.first_name

    user = get_user(user_id)
    rank_pipeline = [{"$sort": {"balance": -1}}, {"$group": {"_id": None, "users": {"$push": "$user_id"}}}]
    rank_data = list(users.aggregate(rank_pipeline))
    rank = 1
    if rank_data and rank_data[0]["users"]:
        try:
            rank = rank_data[0]["users"].index(user_id) + 1
        except ValueError:
            rank = len(rank_data[0]["users"]) + 1
    status = "☠️ Dead" if user.get("killed") else "Alive"

    await update.message.reply_text(
        f"👤 𝐍𝐚𝐦𝐞: {name}\n"
        f"💰 𝐁𝐚𝐥𝐚𝐧𝐜𝐞: ${user['balance']}\n"
        f"🏆 𝐆𝐥𝐨𝐛𝐚𝐥 𝐑𝐚𝐧𝐤: #{rank}\n"
        f"❤️ 𝐒𝐭𝐚𝐭𝐮𝐬: {status}\n"
        f"⚔️ 𝐊𝐢𝐥𝐥𝐬: {user['kills']}"
    )

# Work command
async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user = get_user(update.effective_user.id)
    reward = 200
    users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": reward}})
    await update.message.reply_text(f"💼 You worked and earned {reward} coins!")

# Test command
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ You are not authorized!")
    await update.message.reply_text("✅ Bot is working! Owner confirmed.")

# Bot added/removed
async def my_chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_status = update.my_chat_member.new_chat_member.status
    chat = update.effective_chat
    if new_status in ["member", "administrator"]:
        await send_log_message(context.bot, f"🤖 Bot added to group: {chat.title} ({chat.id})")
    elif new_status == "left":
        await send_log_message(context.bot, f"👋 Bot removed from group: {chat.title} ({chat.id})")

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"⚠️ Error: {context.error}")

# Owner log commands
async def setlog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return await update.message.reply_text("❌ Only owner!")
    chat_id = update.effective_chat.id
    settings.update_one({"_id": "log_chat"}, {"$set": {"chat_id": chat_id}}, upsert=True)
    await update.message.reply_text(f"✅ Log chat set! (Chat ID: <code>{chat_id}</code>)", parse_mode='HTML')

async def dellog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return await update.message.reply_text("❌ Only owner!")
    settings.delete_one({"_id": "log_chat"})
    await update.message.reply_text("🗑️ Log chat deleted.", parse_mode='HTML')

async def testlog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return await update.message.reply_text("❌ Only owner!")
    await send_log_message(context.bot, "✅ Test log message from bot!")

# Main
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_error_handler(error_handler)

    # Track users
    app.add_handler(MessageHandler(~filters.COMMAND, track_users))

    # Start command
    async def start_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await start_command(update, context)
    app.add_handler(CommandHandler("start", start_wrapper))

    # Owner log commands
    app.add_handler(CommandHandler("setlog", setlog))
    app.add_handler(CommandHandler("dellog", dellog))
    app.add_handler(CommandHandler("testlog", testlog))

    # Main commands
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler(["balance", "bal"], balance))
    app.add_handler(CommandHandler("work", work))
    app.add_handler(CommandHandler("economy", economy_guide))
    app.add_handler(CommandHandler("transfer", transfer_balance))
    app.add_handler(CommandHandler("claim", claim))
    app.add_handler(CommandHandler("own", own))
    app.add_handler(CommandHandler("crush", crush))
    app.add_handler(CommandHandler("love", love))
    app.add_handler(CommandHandler("slap", slap))
    app.add_handler(CommandHandler("items", items))
    app.add_handler(CommandHandler("item", item))
    app.add_handler(CommandHandler("give", give))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("rob", rob))
    app.add_handler(CommandHandler("protect", protect))
    app.add_handler(CommandHandler("toprich", toprich))
    app.add_handler(CommandHandler("topkill", topkill))
    app.add_handler(CommandHandler("kill", kill))
    app.add_handler(CommandHandler("revive", revive))
    app.add_handler(CommandHandler("open", open_economy))
    app.add_handler(CommandHandler("close", close_economy))
    app.add_handler(CommandHandler("punch", punch))
    app.add_handler(CommandHandler("hug", hug))
    app.add_handler(CommandHandler("couple", couple))
    app.add_handler(CommandHandler("test", test))

    # Bot added/removed logs
    app.add_handler(ChatMemberHandler(my_chat_member_update, ChatMemberHandler.MY_CHAT_MEMBER))

    print("🚀 Bot Started... Polling mode active")
    app.run_polling()

if __name__ == "__main__":
    main()
