import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# Helpers
from helpers import get_user, users, add_group_user

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# START + BUTTON HANDLER
from commands.start_command import start_command, button_handler

# ECONOMY
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
from commands.punch import punch  # ✅ Import punch command

# Fun commands
from commands.hug import hug
from commands.couple import couple

# -------------------- TRACK GROUP USERS --------------------
async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        user = update.effective_user
        add_group_user(update.effective_chat.id, user.id, user.first_name)

# -------------------- BALANCE COMMAND --------------------
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    rank_pipeline = [
        {"$sort": {"balance": -1}},
        {"$group": {"_id": None, "users": {"$push": "$user_id"}}}
    ]
    rank_data = list(users.aggregate(rank_pipeline))

    if rank_data and rank_data[0]["users"]:
        try:
            rank = rank_data[0]["users"].index(update.effective_user.id) + 1
        except ValueError:
            rank = len(rank_data[0]["users"]) + 1
    else:
        rank = 1

    status = "☠️ Dead" if user.get("killed") else "Alive"
    name = update.effective_user.first_name

    await update.message.reply_text(
        f"👤 𝐍𝐚𝐦𝐞: {name}\n"
        f"💰 𝐁𝐚𝐥𝐚𝐧𝐜𝐞: ${user['balance']}\n"
        f"🏆 𝐆𝐥𝐨𝐛𝐚𝐥 𝐑𝐚𝐧𝐤: #{rank}\n"
        f"❤️ 𝐒𝐭𝐚𝐭𝐮𝐬: {status}\n"
        f"⚔️ 𝐊𝐢𝐥𝐥𝐬: {user['kills']}"
    )

# -------------------- WORK COMMAND --------------------
async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    reward = 200

    users.update_one(
        {"user_id": user["user_id"]},
        {"$inc": {"balance": reward}}
    )

    await update.message.reply_text(f"💼 You worked and earned {reward} coins!")

# -------------------- ERROR HANDLER --------------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"⚠️ Error: {context.error}")
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("❌ Something went wrong!")

# -------------------- MAIN --------------------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_error_handler(error_handler)

    # Track group users
    app.add_handler(MessageHandler(filters.ALL, track_users))

    # Main commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("balance", balance))
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

    # Fun commands
    app.add_handler(CommandHandler("punch", punch))
    app.add_handler(CommandHandler("hug", hug))
    app.add_handler(CommandHandler("couple", couple))

    print("🚀 Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
