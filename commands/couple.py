from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user
import random

async def couple(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ This command works only in groups!")

    all_users = [m.user for m in await context.bot.get_chat_administrators(update.effective_chat.id)]
    if len(all_users) < 2:
        return await update.message.reply_text("❌ Not enough members to form couples!")

    couple = random.sample(all_users, 2)
    await update.message.reply_text(f"💞 Couple: {couple[0].first_name} ❤️ {couple[1].first_name}")
