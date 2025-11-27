from telegram import Update
from telegram.ext import ContextTypes
from helpers import set_group_status

# commands/close.py
async def close_cmd(update, context):
    await update.message.reply_text("❌ Economy commands are now CLOSED in this group!")

