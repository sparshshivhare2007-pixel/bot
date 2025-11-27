from telegram import Update
from telegram.ext import ContextTypes

async def slap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to someone to slap them!")

    target_name = update.message.reply_to_message.from_user.first_name
    await update.message.reply_text(f"👊 You slapped {target_name}!")
