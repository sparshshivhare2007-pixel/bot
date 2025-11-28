# group_management.py
from telegram import Update, ChatPermissions
from telegram.ext import CommandHandler, ContextTypes, Application
from telegram.constants import ChatMemberStatus

# Helper to check admin
async def is_user_admin(update: Update, user_id: int):
    member = await update.effective_chat.get_member(user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]

# Kick command
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ This command works only in groups!")

    if not await is_user_admin(update, user.id):
        return await update.message.reply_text("⛔ You must be an admin to use this command!")

    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to the user you want to kick.")

    target = update.message.reply_to_message.from_user
    try:
        await chat.kick_member(target.id)
        await update.message.reply_text(f"✅ {target.full_name} has been kicked!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to kick: {e}")

# Mute command
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ This command works only in groups!")

    if not await is_user_admin(update, user.id):
        return await update.message.reply_text("⛔ You must be an admin to use this command!")

    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to the user you want to mute.")

    target = update.message.reply_to_message.from_user
    try:
        await chat.restrict_member(target.id, permissions=ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"✅ {target.full_name} has been muted!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to mute: {e}")

# Register all group management handlers
def register_group_management(app: Application):
    app.add_handler(CommandHandler("kick", kick))
    app.add_handler(CommandHandler("mute", mute))
    # add more like ban, unmute, lock, unlock, purge
