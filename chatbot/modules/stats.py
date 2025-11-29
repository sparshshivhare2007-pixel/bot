from telegram import Update
from telegram.ext import ContextTypes
from chatbot.helpers import get_stats

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = await get_stats()
    await update.message.reply_text(
        f"📊 Bot Stats:\nUsers: {data['users']}\nChats: {data['chats']}"
    )
