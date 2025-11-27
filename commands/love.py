from telegram import Update
from telegram.ext import ContextTypes
from helpers import random_percentage

async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to someone to check your love %.")

    target_name = update.message.reply_to_message.from_user.first_name
    percent = random_percentage()
    await update.message.reply_text(f"❤️ Love Percentage with {target_name}: {percent}%")
