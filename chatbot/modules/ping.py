from telegram import Update
from telegram.ext import ContextTypes
from chat.chat_helpers import get_chat_user, add_message

import random

STICKERS = [
    "CAACAgIAAxkBAAEBFhlgU6mF2yZzZcFZ_LfqvYhJvGgczAACnQEAAladvQpY1c4C7K2aACkE",
    "CAACAgIAAxkBAAEBFhlgU6mF2yZzZcFZ_LfqvYhJvGgczAACnQEAAladvQpY1c4C7K2aACkE"
]

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    get_chat_user(user_id)  # Ensure user exists
    await update.message.reply_sticker(random.choice(STICKERS))
    await update.message.reply_text("Bot is alive! ✅")
