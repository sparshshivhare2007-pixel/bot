from telegram import Update
from telegram.ext import ContextTypes
from chat.chat_helpers import get_chat_user, add_message, is_user_exists

async def chat_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text
    if not is_user_exists(user_id):
        get_chat_user(user_id)
    add_message(user_id, message)
    # Example AI response
    await update.message.reply_text(f"You said: {message}")
