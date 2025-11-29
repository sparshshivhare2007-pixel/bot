import os
from telegram import Update
from telegram.ext import ContextTypes

OWNER_ID = int(os.getenv("OWNER_ID", 0))

async def eval_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ Not authorized!")

    code = " ".join(context.args)
    try:
        result = eval(code)
        await update.message.reply_text(f"✅ Result:\n{result}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{e}")
