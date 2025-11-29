from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from helpers import get_user, add_group_id, users

import random

# Photos for leave messages
photos = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg"
]

async def on_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    for member in update.message.new_chat_members:
        # Bot join nahi count
        if member.is_bot:
            continue
        add_group_id(chat.id)
        await context.bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=f"✅ New Member in {chat.title} ({chat.id}): {member.mention}"
        )

async def on_left_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    left_member = update.message.left_chat_member
    if left_member:
        await context.bot.send_photo(
            chat_id=LOG_GROUP_ID,
            photo=random.choice(photos),
            caption=f"❌ Member Left {chat.title} ({chat.id}): {left_member.mention}"
        )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num_users = len(users)
    await update.message.reply_text(
        f"📊 Bot Status:\n"
        f"👥 Users: {num_users}\n"
        f"💬 Groups: {len(add_group_id)}"
    )

def register_welcome_status(app):
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_new_member))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, on_left_member))
    app.add_handler(CommandHandler("status", status_command))
