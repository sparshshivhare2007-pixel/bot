from telegram import Update
from telegram.ext import ContextTypes

async def chatbot_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm your friendly chatbot 😊\nHow can I help you today?"
    )
