# group_management.py
from telegram import Update, ChatPermissions
from telegram.ext import CommandHandler, Application, ContextTypes, MessageHandler, filters
from telegram.constants import ChatMemberStatus

# Dictionary to track warnings
warnings = {}

# Helper to check if user is admin
async def is_user_admin(update: Update, user_id: int):
    member = await update.effective_chat.get_member(user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]

# ------------------ KICK ------------------
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

# ------------------ BAN ------------------
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ This command works only in groups!")

    if not await is_user_admin(update, user.id):
        return await update.message.reply_text("⛔ You must be an admin to use this command!")

    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to the user you want to ban.")

    target = update.message.reply_to_message.from_user
    try:
        await chat.ban_member(target.id)
        await update.message.reply_text(f"✅ {target.full_name} has been banned!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to ban: {e}")

# ------------------ UNBAN ------------------
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ This command works only in groups!")

    if not await is_user_admin(update, user.id):
        return await update.message.reply_text("⛔ You must be an admin to use this command!")

    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to the user you want to unban.")

    target = update.message.reply_to_message.from_user
    try:
        await chat.unban_member(target.id)
        await update.message.reply_text(f"✅ {target.full_name} has been unbanned!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to unban: {e}")

# ------------------ MUTE ------------------
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

# ------------------ UNMUTE ------------------
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ This command works only in groups!")

    if not await is_user_admin(update, user.id):
        return await update.message.reply_text("⛔ You must be an admin to use this command!")

    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to the user you want to unmute.")

    target = update.message.reply_to_message.from_user
    try:
        await chat.restrict_member(target.id, permissions=ChatPermissions(can_send_messages=True))
        await update.message.reply_text(f"✅ {target.full_name} has been unmuted!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to unmute: {e}")

# ------------------ LOCK ------------------
async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Only in groups!")
    if not await is_user_admin(update, user.id):
        return await update.message.reply_text("⛔ Admins only!")
    try:
        await chat.set_permissions(ChatPermissions(can_send_messages=False))
        await update.message.reply_text("🔒 Group has been locked!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to lock: {e}")

# ------------------ UNLOCK ------------------
async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Only in groups!")
    if not await is_user_admin(update, user.id):
        return await update.message.reply_text("⛔ Admins only!")
    try:
        await chat.set_permissions(ChatPermissions(can_send_messages=True))
        await update.message.reply_text("🔓 Group has been unlocked!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to unlock: {e}")

# ------------------ WARN ------------------
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Only in groups!")
    if not await is_user_admin(update, user.id):
        return await update.message.reply_text("⛔ Admins only!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to the user you want to warn.")

    target = update.message.reply_to_message.from_user
    warnings[target.id] = warnings.get(target.id, 0) + 1
    await update.message.reply_text(f"⚠️ {target.full_name} has been warned! Total: {warnings[target.id]}")

# ------------------ PURGE ------------------
async def purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Only in groups!")
    if not await is_user_admin(update, user.id):
        return await update.message.reply_text("⛔ Admins only!")

    args = context.args
    if not args or not args[0].isdigit():
        return await update.message.reply_text("❌ Usage: /purge <number_of_messages> (reply optional)")

    count = int(args[0])
    async for message in chat.get_history(limit=count):
        try:
            await message.delete()
        except:
            continue
    await update.message.reply_text(f"✅ {count} messages deleted!")

# ------------------ REGISTER HANDLERS ------------------
def register_group_management(app: Application):
    app.add_handler(CommandHandler("kick", kick))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("lock", lock))
    app.add_handler(CommandHandler("unlock", unlock))
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("purge", purge))
