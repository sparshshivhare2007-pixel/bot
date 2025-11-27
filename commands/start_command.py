from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ApplicationBuilder

# /start command
async def start_command(update: Update, context: CallbackContext):
    user = update.effective_user

    text = (
        f"✨ Hey {user.first_name} ~\n"
        "💞 You're talking to *𝐀𝐤𝐞𝐧𝐨*, a sassy cutie bot 💕\n\n"
        "☑ Choose an option below:"
    )

    keyboard = [
        [InlineKeyboardButton("💬 Talk to 𝐀𝐤𝐞𝐧𝐨", callback_data="talk")],
        [
            InlineKeyboardButton("🧸 Friends", url="https://t.me/mich_family_group")
            InlineKeyboardButton("🎮 Games", callback_data="games")
        ],
        [InlineKeyboardButton("👥 Add me to your group", url="https://t.me/YourBot?startgroup=true")]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Callback query handler
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Ye zaruri hai Telegram ko notify karne ke liye ki button press hua

    if query.data == "friends":
        # Yaha pe tumhara group ka link bhej rahe
        await query.message.reply_text(
            "Join my awesome group! 👥\n👉 [Click Here](https://t.me/mich_family_group)",
            parse_mode="Markdown"
        )
    elif query.data == "talk":
        await query.message.reply_text("Let's chat! 💬")
    elif query.data == "games":
        await query.message.reply_text("Check out the games! 🎮")

#
