# commands/group_management.py
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, Application, filters, MessageHandler

# In-memory storage for warnings
warnings_db = {}

# Admin check helper
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await update.effective_chat.get_member(update.effective_user.id)
    return member.status in ["administrator", "creator"]

# /warn command
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("⛔ Only admins can warn users.")
    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to the user you want to warn.")
    
    user_id = update.message.reply_to_message.from_user.id
    reason = " ".join(context.args) or "No reason"
    warnings_db[user_id] = warnings_db.get(user_id, 0) + 1
    await update.message.reply_text(
        f"⚠️ {update.message.reply_to_message.from_user.first_name} has been warned.\n"
        f"Reason: {reason}\n"
        f"Total Warnings: {warnings_db[user_id]}"
    )

# /warnings command
async def check_warnings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to the user to check warnings.")
    user_id = update.message.reply_to_message.from_user.id
    total = warnings_db.get(user_id, 0)
    await update.message.reply_text(f"⚠️ {update.message.reply_to_message.from_user.first_name} has {total} warning(s).")

# /kick command
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("⛔ Only admins can kick users.")
    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to the user to kick.")
    user = update.message.reply_to_message.from_user
    await update.effective_chat.kick_member(user.id)
    await update.message.reply_text(f"👢 {user.first_name} has been kicked from the group.")

# Function to register handlers
def register_group_management(app: Application):
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("warnings", check_warnings))
    app.add_handler(CommandHandler("kick", kick))
    # Add more handlers like /ban, /mute, /lock, etc. similarly
