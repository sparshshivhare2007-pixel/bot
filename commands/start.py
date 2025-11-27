from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat
    user = update.effective_user
    name = user.first_name

    # If user is in GROUP
    if chat.type in ["group", "supergroup"]:
        await update.message.reply_text(
            f"👋 Hello {name}!\n"
            "✨ I'm alive and ready!\n"
            "Use /balance or other commands."
        )
        return

    # If user is in PRIVATE CHAT (DM)
    buttons = [
        [InlineKeyboardButton("💬 Talk to Baka", callback_data="talk")],
        [
            InlineKeyboardButton("🧸 Friends", callback_data="friends"),
            InlineKeyboardButton("🎮 Games", callback_data="games"),
        ],
        [InlineKeyboardButton("➕ Add me to your group 👥", url=f"https://t.me/{context.bot.username}?startgroup=true")]
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    text = (
        f"✨ Hey {name}!\n"
        "💗 You're talking to **𝐀𝐤𝐞𝐧𝐨**, a sassy cutie bot 💕\n\n"
        "⬇ Choose an option below:"
    )

    # Markdown V2 safe formatting
    text = text.replace("_", "\\_").replace("*", "\\*")

    await update.message.reply_text(
        text,
        reply_markup=keyboard,
        parse_mode="MarkdownV2"
    )
