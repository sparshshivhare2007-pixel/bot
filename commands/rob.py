from telegram import Update
from telegram.ext import ContextTypes
from utils import get_user, users  # your DB functions
from datetime import datetime
from random import randint

async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to someone to rob them!")

    user_id = update.effective_user.id
    target_id = update.message.reply_to_message.from_user.id

    if user_id == target_id:
        return await update.message.reply_text("❌ You cannot rob yourself!")

    robber = get_user(user_id)
    target = get_user(target_id)

    amount = randint(1, min(1000, target["balance"]))

    if "protection" in target and target["protection"] > datetime.utcnow():
        return await update.message.reply_text("🛡 Target is protected!")

    if target["balance"] <= 0:
        return await update.message.reply_text("❌ Target has no coins!")

    # Update balances
    users.update_one({"user_id": user_id}, {"$inc": {"balance": amount}})
    users.update_one({"user_id": target_id}, {"$inc": {"balance": -amount}})

    await update.message.reply_text(f"💰 You robbed {amount} coins from {update.message.reply_to_message.from_user.first_name}!")
