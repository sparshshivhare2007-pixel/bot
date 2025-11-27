from telegram import Update
from telegram.ext import ContextTypes
from utils import get_user, users
from datetime import datetime, timedelta

async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    args = context.args
    if not args or args[0] not in ["1d", "2d"]:
        return await update.message.reply_text("Usage: /protect 1d or /protect 2d")

    days = int(args[0][0])
    cost = 500 * days

    if user["balance"] < cost:
        return await update.message.reply_text(f"❌ You need {cost} coins!")

    users.update_one({"user_id": user_id}, {"$set": {"balance": user["balance"]-cost, "protection": datetime.utcnow() + timedelta(days=days)}})

    await update.message.reply_text(f"🛡 Protection active for {days} day(s)! 💰 Remaining balance: {user['balance']-cost}")
