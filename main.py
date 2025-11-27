import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from helpers import get_user, users

# Load ENV
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# -------------------- IMPORT START COMMAND --------------------
from commands.start_command import start_command

# -------------------- BASIC COMMANDS --------------------

async def balance(update, context):
    user = get_user(update.effective_user.id)

    # Global Rank Calculation
    rank_pipeline = [
        {"$sort": {"balance": -1}},
        {"$group": {"_id": None, "users": {"$push": "$user_id"}}}
    ]

    rank_data = list(users.aggregate(rank_pipeline))
    rank = rank_data[0]["users"].index(update.effective_user.id) + 1 if rank_data else 1

    status = "☠️ Dead" if user.get("killed") else "Alive"
    name = update.effective_user.first_name

    await update.message.reply_text(
        f"👤 Name: {name}\n"
        f"💰 Total Balance: ${user['balance']}\n"
        f"🏆 Global Rank: #{rank}\n"
        f"❤️ Status: {status}\n"
        f"⚔️ Kills: {user['kills']}"
    )


async def work(update, context):
    user = get_user(update.effective_user.id)
    reward = 200

    users.update_one(
        {"user_id": user["user_id"]},
        {"$inc": {"balance": reward}}
    )

    await update.message.reply_text(f"💼 You worked and earned {reward} coins!")


# -------------------- IMPORT ALL OTHER COMMANDS --------------------
from commands.claim import claim
from commands.own import own
from commands.couple import couple
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


# -------------------- RUN BOT --------------------
def main():
    app = Application.builder().token(TOKEN).build()

    # ---- CUSTOM START HANDLER FROM start.py ----
    app.add_handler(CommandHandler("start", start_command))

    # Basic
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("work", work))

    # Imported commands
    app.add_handler(CommandHandler("claim", claim))
    app.add_handler(CommandHandler("own", own))
    app.add_handler(CommandHandler("couple", couple))
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

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
