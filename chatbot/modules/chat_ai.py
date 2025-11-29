from chatbot.helpers import add_served_chat, add_served_user
from telegram import Update
from telegram.ext import ContextTypes

async def chat_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_msg = message.text

    # Example simple friendly AI reply
    reply = f"Hey {message.from_user.first_name}, you said: {user_msg}\nI'm here to chat with you 😊"

    await message.reply_text(reply)

    # Track user/chat for database
    if message.chat.type == "private":
        await add_served_user(message.from_user.id)
    else:
        await add_served_chat(message.chat.id)
