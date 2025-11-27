from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user, is_group_open, users

async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group_open(update.effective_chat.id):
        return await update.message.reply_text("❌ Economy commands are closed in this group!")

    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to the user you want to kill.")

    killer_id = update.effective_user.id
    target_id = update.message.reply_to_message.from_user.id

    if killer_id == target_id:
        return await update.message.reply_text("❌ You cannot kill yourself!")

    target = get_user(target_id)

    if target.get("killed", False):
        return await update.message.reply_text("❌ This user is already killed. Revive them!")

    users.update_one({"user_id": killer_id}, {"$inc": {"kills": 1}})
    users.update_one({"user_id": target_id}, {"$set": {"balance": 0, "killed": True}})

    await update.message.reply_text(
        f"⚔️ {update.effective_user.first_name} killed {update.message.reply_to_message.from_user.first_name}!\n"
        f"💀 Balance is now 0 and status set to killed."
    )
