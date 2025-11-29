from telegram import Update
from telegram.ext import ContextTypes

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # simple rules
    if "hello" in text:
        return await update.message.reply_text("Hi! 😊")

    if "kaise ho" in text:
        return await update.message.reply_text("Main bilkul mast! Aur tum? 😄")

    # default reply
    await update.message.reply_text("Hmm, interesting... aur batao?")
