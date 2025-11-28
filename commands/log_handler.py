# log_handler.py
from telegram import Update
from telegram.ext import ContextTypes

LOG_GROUP_ID = -1003356231387  # <-- apna log group id daalna


def mention(user):
    return f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"


# ---------- START LOG ----------
async def log_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    text = (
        f"🚀 <b>Bot Started</b>\n"
        f"👤 User: {mention(user)}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"💬 Chat Type: <b>{chat.type}</b>"
    )

    await context.bot.send_message(
        LOG_GROUP_ID, text, parse_mode="HTML"
    )


# ---------- GROUP ADD LOG ----------
async def log_added_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    text = (
        f"➕ <b>Bot Added to Group</b>\n"
        f"👥 Group: <b>{chat.title}</b>\n"
        f"👤 Added By: {mention(user)}"
    )

    await context.bot.send_message(
        LOG_GROUP_ID, text, parse_mode="HTML"
    )
