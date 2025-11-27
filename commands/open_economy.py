from telegram import Update
from telegram.ext import ContextTypes
from helpers import set_group_status

async def open(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        set_group_status(update.effective_chat.id, True)
        await update.message.reply_text("✅ Economy commands are now OPEN in this group!")
 
