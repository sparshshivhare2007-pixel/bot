import os
import random
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# -------------------- HELPERS --------------------
from helpers import (
    get_user,
    user_db,
    add_group_id,
    runtime_users,
    runtime_groups,
    group_db
)

# -------------------- LOAD ENV --------------------
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0"))

# -------------------- ECONOMY COMMANDS --------------------
from commands.start_command import start_command, button_handler
from commands.group_management import register_group_management
from commands.economy_guide import economy_guide
from commands.help_command import help_command

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
from commands.kiss import kiss

from commands.mine import mine
from commands.farm import farm
from commands.crime import crime
from commands.heal import heal
from commands.shop import shop
from commands.buy import buy
from commands.sell import sell
from commands.profile import profile
from commands.bank import bank
from commands.deposit import deposit
from commands.withdraw import withdraw

# -------------------- CHATBOT COMMANDS --------------------
from chatbot.modules.start_chat import start as chat_start  # Chatbot start
from chatbot.chatbot import register_chat_handlers
from chatbot.broadcast import broadcast
from chatbot.ping import ping

# -------------------- WELCOME PHOTOS --------------------
welcome_photos = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg",
]

# -------------------- ECONOMY HANDLER FUNCTIONS --------------------
async def test_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ You are not authorized.")
    await update.message.reply_text("🔄 Restarting bot...")
    os._exit(1)

async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        add_group_id(chat.id)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        user_id = target.id
        name = target.first_name
    else:
        user_id = update.effective_user.id
        name = update.effective_user.first_name

    user = get_user(user_id)
    rank_data = list(user_db.find().sort("balance", -1))
    ids = [u["user_id"] for u in rank_data]
    try:
        rank = ids.index(user_id) + 1
    except:
        rank = len(ids) + 1

    status = "☠️ Dead" if user.get("killed") else "Alive"

    await update.message.reply_text(
        f"👤 Name: {name}\n"
        f"💰 Balance: ${user.get('balance', 0)}\n"
        f"🏆 Rank: #{rank}\n"
        f"❤️ Status: {status}\n"
        f"⚔️ Kills: {user.get('kills', 0)}"
    )

async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    reward = 200
    user_db.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": reward}})
    await update.message.reply_text(f"💼 You worked and earned {reward} coins!")

async def on_bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not LOG_GROUP_ID:
        return
    if not update.message or not update.message.new_chat_members:
        return

    bot_added = any(m.id == context.bot.id for m in update.message.new_chat_members)
    if not bot_added:
        return

    chat = update.effective_chat
    added_by = update.message.from_user
    try:
        count = await context.bot.get_chat_members_count(chat.id)
    except:
        count = "Unknown"

    username = chat.username if chat.username else "Private Group"

    caption = (
        f"🤖 Bot Added In A New Group\n\n"
        f"Name: {chat.title}\n"
        f"ID: {chat.id}\n"
        f"Username: @{username}\n"
        f"Members: {count}\n"
        f"Added By: {added_by.first_name}"
    )

    try:
        await context.bot.send_photo(
            chat_id=LOG_GROUP_ID,
            photo=random.choice(welcome_photos),
            caption=caption
        )
    except:
        pass

async def on_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not LOG_GROUP_ID:
        return
    if not update.message or not update.message.new_chat_members:
        return

    chat = update.effective_chat
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            continue
        add_group_id(chat.id)
        text = f"✅ New Member in {chat.title}: {member.first_name}"
        try:
            await context.bot.send_message(LOG_GROUP_ID, text)
        except:
            pass

async def on_left_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not LOG_GROUP_ID:
        return
    if not update.message or not update.message.left_chat_member:
        return

    chat = update.effective_chat
    left = update.message.left_chat_member
    caption = f"❌ Member Left {chat.title}: {left.first_name}"
    try:
        await context.bot.send_photo(
            chat_id=LOG_GROUP_ID,
            photo=random.choice(welcome_photos),
            caption=caption
        )
    except:
        pass

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 Bot Status:\n"
        f"👥 Users (active): {len(runtime_users)}\n"
        f"💬 Groups (active): {len(runtime_groups)}"
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"⚠️ Error: {context.error}")
    try:
        if hasattr(update, "effective_message") and update.effective_message:
            await update.effective_message.reply_text("❌ Something went wrong!")
    except:
        pass

# -------------------- MAIN --------------------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_error_handler(error_handler)

    # -------------------- ECONOMY HANDLERS --------------------
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_users))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("test", test_restart))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_bot_added))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_new_member))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, on_left_member))
    app.add_handler(CommandHandler("status", status_command))

    # Economy commands
    economy_commands = [
        ("balance", balance), ("work", work), ("economy", economy_guide),
        ("transfer", transfer_balance), ("claim", claim), ("own", own),
        ("crush", crush), ("love", love), ("slap", slap),
        ("items", items), ("item", item), ("give", give), ("daily", daily),
        ("rob", rob), ("protect", protect), ("toprich", toprich),
        ("topkill", topkill), ("kill", kill), ("revive", revive),
        ("open", open_economy), ("close", close_economy)
    ]
    for cmd, handler in economy_commands:
        app.add_handler(CommandHandler(cmd, handler))

    # Fun
    fun = [("punch", punch), ("hug", hug), ("couple", couple), ("kiss", kiss)]
    for cmd, handler in fun:
        app.add_handler(CommandHandler(cmd, handler))

    # Hidden
    hidden = [
        ("mine", mine), ("farm", farm), ("crime", crime),
        ("heal", heal), ("shop", shop), ("buy", buy), ("sell", sell),
        ("profile", profile), ("bank", bank), ("deposit", deposit),
        ("withdraw", withdraw)
    ]
    for cmd, handler in hidden:
        app.add_handler(CommandHandler(cmd, handler))

    # Group management
    register_group_management(app)

    # -------------------- CHATBOT HANDLERS --------------------
    # Chatbot start command mapped to /chatstart
    app.add_handler(CommandHandler("chatstart", chat_start))
    register_chat_handlers(app)

    print("🚀 Bot Started Successfully!")
    app.run_polling()

if __name__ == "__main__":
    main()
