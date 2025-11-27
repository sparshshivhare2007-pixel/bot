from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def start_command(update: Update, context: CallbackContext):
    user = update.effective_user

    text = (
        f"✨ Hey  {user.first_name} ~\n"
        "💞 You're talking to *𝐀𝐤𝐞𝐧𝐨*, a sassy cutie bot 💕\n\n"
        "☑ Choose an option below:"
    )

    keyboard = [
        [InlineKeyboardButton("💬 Talk to 𝐀𝐤𝐞𝐧𝐨", callback_data="talk")],
        [
            InlineKeyboardButton("🧸 Friends", callback_data="friends"),
            InlineKeyboardButton("🎮 Games", callback_data="games")
        ],
        [InlineKeyboardButton("👥 Add me to your group", url="https://t.me/YourBot?startgroup=true")]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
