from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

# ------------------ HELPER: CHECK ADMIN ------------------
async def is_admin(update, user_id):
    chat = update.effective_chat
    member = await chat.get_member(user_id)
    return member.status in ["administrator", "creator"]

# ------------------ HELPER: GET TARGET USER ------------------
async def get_target_user(update, context):
    # Reply
    if update.message.reply_to_message:
        return update.message.reply_to_message.from_user

    # Try from args (username or ID)
    if context.args:
        try:
            user = await update.get_bot().get_chat(context.args[0])
            return user
        except:
            return None

    return None

# ==========================================================
#                         BAN
# ==========================================================
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Use this in groups only.")

    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ Only admins can ban users.")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found.")

    try:
        await chat.ban_member(target.id)
        await update.message.reply_text(f"🚫 {target.full_name} has been banned!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ==========================================================
#                        UNBAN
# ==========================================================
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Use this command in groups only.")

    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ Only admins can unban users.")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found.")

    try:
        await chat.unban_member(target.id, only_if_banned=True)
        await update.message.reply_text(
            f"✅ {target.full_name} has been unbanned.\n"
            "Now they can rejoin the group."
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ==========================================================
#                         MUTE
# ==========================================================
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Group only command.")

    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ Only admins can mute.")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found.")

    try:
        perms = ChatPermissions(can_send_messages=False)
        await chat.restrict_member(target.id, permissions=perms)

        await update.message.reply_text(
            f"🔇 {target.full_name} has been muted."
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ==========================================================
#                        UNMUTE
# ==========================================================
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Group only command.")

    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ Only admins can unmute.")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found.")

    try:
        perms = ChatPermissions(can_send_messages=True)
        await chat.restrict_member(target.id, permissions=perms)

        await update.message.reply_text(
            f"🔊 {target.full_name} has been unmuted."
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ==========================================================
#                         WARN
# ==========================================================
# Temporary warn storage (in-memory)
warns = {}  # {chat_id: {user_id: warn_count}}

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    cid = chat.id

    if cid not in warns:
        warns[cid] = {}

    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ Only admins can warn users.")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found.")

    uid = target.id
    warns[cid][uid] = warns[cid].get(uid, 0) + 1

    count = warns[cid][uid]

    await update.message.reply_text(
        f"⚠️ {target.first_name} warned! ({count}/3)"
    )

    # Auto ban at 3 warns
    if count >= 3:
        try:
            await chat.ban_member(uid)
            await update.message.reply_text(f"🚫 {target.full_name} auto-banned (3 warns)!")
        except:
            pass

# ==========================================================
#                        UNWARN
# ==========================================================
async def unwarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    cid = chat.id

    if cid not in warns:
        warns[cid] = {}

    if not await is_admin(update, update.effective_user.id):
        return await update.message.reply_text("⛔ Only admins can unwarn users.")

    target = await get_target_user(update, context)
    if not target:
        return await update.message.reply_text("❌ User not found.")

    uid = target.id

    if warns[cid].get(uid, 0) == 0:
        return await update.message.reply_text("ℹ️ User has no warnings.")

    warns[cid][uid] -= 1

    await update.message.reply_text(
        f"✅ Removed a warning from {target.first_name}. ({warns[cid][uid]}/3)"
    )

# ==========================================================
#                REGISTER HANDLERS FOR MAIN.PY
# ==========================================================
def register_group_management(app):
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("unwarn", unwarn))
