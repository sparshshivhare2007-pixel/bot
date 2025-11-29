from telegram.ext import Application
from chatbot.ping import ping
from chatbot.chat_ai import chat_ai

def register_chat_handlers(app: Application):
    # Register ping
    from telegram.ext import CommandHandler, MessageHandler, filters

    app.add_handler(CommandHandler("ping", ping))

    # Register chat AI for all text messages in private chats
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, chat_ai))
