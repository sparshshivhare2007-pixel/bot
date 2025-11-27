from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user, is_group_open, users
import random

async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group_open(update.effective_chat.id):
        return await update.message.reply_text("❌ Economy commands are closed in this group!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to the user you want to rob.")

    user = get_user(update.effective_user.id)
    target_user_id = update.message.reply_to_message.from_user.id
    target = get_user(target_user_id)

    if target["balance"] <= 0:
        return await update.message.reply_text("❌ Target has no coins!")

    amount = random.randint(1, min(1000, target["balance"]))
    users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": amount}})
    users.update_one({"user_id": target_user_id}, {"$inc": {"balance": -amount}})
    await update.message.reply_text(f"💸 You robbed {amount} coins!")
