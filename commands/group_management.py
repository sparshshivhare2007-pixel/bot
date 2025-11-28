from telegram import Update, ChatPermissions
from telegram.ext import CommandHandler, Application, ContextTypes
from telegram.constants import ChatMemberStatus

# In-memory warnings storage
warnings = {}

# ------------------ Helper ------------------
async def get_target_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Returns target user either by reply or by argument (id/username)
    """
    if update.message.reply_to_message:
        return update.message.reply_to_message.from_user
    elif context.args:
        arg = context.args[0]
        chat_members = await update.effective_chat.get_administrators()
        try:
            # Try by user_id
            user_id = int(arg)
            member = await update.effective_chat.get_member(user_id)
            return member.user
        except ValueError:
            # Try by username (without @)
            username = arg.replace("@", "")
            for member in chat_members + [await update.effective_chat.get_member(update.effective_user.id)]:
                if member.user.username == username:
                    return member.user
    return None

async def is_admin(update: Update, user_id: int):
    member = await update.effective_chat.get_member(user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]

# ------------------ BAN ------------------
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Only in groups!")
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ You must be an admin!")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found! Reply or provide username/id.")

    try:
        await update.effective_chat.ban_member(target.id)
        await update.message.reply_text(f"✅ {target.full_name} has been banned!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ------------------ UNBAN ------------------
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Only in groups!")
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ You must be an admin!")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found! Reply or provide username/id.")

    try:
        await update.effective_chat.unban_member(target.id)
        await update.message.reply_text(f"✅ {target.full_name} has been unbanned!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ------------------ MUTE ------------------
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Only in groups!")
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ Admins only!")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found!")

    try:
        await update.effective_chat.restrict_member(
            target.id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text(f"✅ {target.full_name} has been muted!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ------------------ UNMUTE ------------------
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Only in groups!")
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ Admins only!")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found!")

    try:
        await update.effective_chat.restrict_member(
            target.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await update.message.reply_text(f"✅ {target.full_name} has been unmuted!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ------------------ WARN ------------------
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Only in groups!")
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ Admins only!")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found!")

    warnings[target.id] = warnings.get(target.id, 0) + 1
    await update.message.reply_text(f"⚠️ {target.full_name} has been warned! Total warnings: {warnings[target.id]}")

# ------------------ UNWARN ------------------
async def unwarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Only in groups!")
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ Admins only!")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found!")

    if warnings.get(target.id):
        warnings[target.id] -= 1
        await update.message.reply_text(f"✅ {target.full_name} has been unwarned! Total warnings: {warnings[target.id]}")
    else:
        await update.message.reply_text(f"ℹ️ {target.full_name} has no warnings.")

# ------------------ REGISTER HANDLERS ------------------
def register_group_management(app: Application):
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("unwarn", unwarn))
