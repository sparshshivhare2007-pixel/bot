from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}!\n"
        "I am your friendly ChatBot. 🤖\n"
        "You can chat with me or use /ping to check if I'm alive!"
    )
