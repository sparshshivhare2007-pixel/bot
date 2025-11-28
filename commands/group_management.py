from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

# Warn storage (You can replace with database later)
user_warnings = {}

# Helper: check admin
async def is_admin(update: Update, user_id: int):
    chat_admins = await update.effective_chat.get_administrators()
    admin_ids = [admin.user.id for admin in chat_admins]
    return user_id in admin_ids


# ------------------ BAN ------------------
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("❌ You must be admin to use this.")

    # get user from reply or args
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        user_id = int(context.args[0])
    else:
        return await update.message.reply_text("⚠ Reply or give User ID to /ban")

    await update.effective_chat.ban_member(user_id)
    await update.message.reply_text("🚫 User has been *banned* successfully!", parse_mode="HTML")


# ------------------ UNBAN ------------------
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("❌ You must be admin to use this.")

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        user_id = int(context.args[0])
    else:
        return await update.message.reply_text("⚠ Reply or give User ID to /unban")

    await update.effective_chat.unban_member(user_id)
    await update.message.reply_text("✅ User has been *unbanned* and can join again.", parse_mode="HTML")


# ------------------ MUTE ------------------
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("❌ Admin required.")

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        user_id = int(context.args[0])
    else:
        return await update.message.reply_text("⚠ Reply or give User ID to /mute")

    perms = ChatPermissions(can_send_messages=False)
    await update.effective_chat.restrict_member(user_id, perms)

    await update.message.reply_text("🔇 User has been *muted*.", parse_mode="HTML")


# ------------------ UNMUTE ------------------
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("❌ Admin required.")

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        user_id = int(context.args)[0]
    else:
        return await update.message.reply_text("⚠ Reply or give User ID to /unmute")

    perms = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )
    await update.effective_chat.restrict_member(user_id, perms)

    await update.message.reply_text("🔊 User has been *unmuted*.", parse_mode="HTML")


# ------------------ WARN ------------------
async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("❌ Admin required.")

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        return await update.message.reply_text("⚠ Reply to user to /warn")

    user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

    await update.message.reply_text(
        f"⚠ Warning issued.\nTotal Warnings: {user_warnings[user_id]}"
    )


# ------------------ UNWARN ------------------
async def unwarn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("❌ Admin required.")

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        return await update.message.reply_text("⚠ Reply to user to /unwarn")

    if user_id in user_warnings and user_warnings[user_id] > 0:
        user_warnings[user_id] -= 1

    await update.message.reply_text(
        f"✅ Warning removed.\nRemaining Warnings: {user_warnings.get(user_id, 0)}"
    )
