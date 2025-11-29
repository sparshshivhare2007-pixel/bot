from telegram import Update
from telegram.ext import ContextTypes
from chat.chat_helpers import get_chat_user, is_user_exists  # <- helpers import

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Ensure user exists in chat DB
    if not is_user_exists(user_id):
        get_chat_user(user_id)

    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}!\n"
        "I am your friendly ChatBot. 🤖\n"
        "You can chat with me or use /ping to check if I'm alive!"
    )
