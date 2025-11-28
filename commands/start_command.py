from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

BOT_IMAGE_URL = "https://files.catbox.moe/z1skp4.jpg"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    keyboard = [
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("About", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = f"Hello {user.first_name}!\nWelcome to the bot ❤️"

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=BOT_IMAGE_URL,
        caption=caption,
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        await query.edit_message_text("This is the help section.")
    elif query.data == "about":
        await query.edit_message_text("This bot is created for testing.")
