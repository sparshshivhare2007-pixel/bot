from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes

# /sticker_id command start
async def sticker_id_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Apna sticker bhejo aur main uska ID bata dunga!")

# Sticker receive handler
async def sticker_id_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.sticker:
        file_id = update.message.sticker.file_id
        await update.message.reply_text(f"✅ Sticker ID: `{file_id}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Sirf sticker bhejo!")

# Function to register handlers in main.py
def register_sticker_id_handlers(app):
    app.add_handler(CommandHandler("sticker_id", sticker_id_start))
    app.add_handler(MessageHandler(filters.STICKER & ~filters.COMMAND, sticker_id_receive))
