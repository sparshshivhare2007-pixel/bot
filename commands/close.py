from telegram import Update
from telegram.ext import ContextTypes
from helpers import set_group_status

async def close(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        set_group_status(update.effective_chat.id, False)
        await update.message.reply_text("❌ Economy commands are now CLOSED in this group!")
