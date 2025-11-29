# Simple command to show user ID / chat ID
from telegram import Update
from telegram.ext import ContextTypes

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    await update.message.reply_text(
        f"User ID: {user.id}\nChat ID: {chat.id}"
    )
