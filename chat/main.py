from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from .helpers import get_chat_response

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Hello! I'm your ChatBot. Ask me anything.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = get_chat_response(user_message)
    await update.message.reply_text(response)

def register_chat_handlers(app):
    """Register chatbot handlers"""
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
