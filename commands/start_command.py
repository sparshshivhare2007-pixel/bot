# commands/start_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes  # Use ContextTypes for async PTB v20+

# 🚨 IMPORTANT: Replace this URL with the direct link to your bot's welcome image
BOT_IMAGE_URL = "https://files.catbox.moe/z1skp4.jpg"

# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    text = (
        f"👋 Hey, →🪬{user.first_name}🪬🤍\n"
        "💞 You're talking to *𝐀𝐤e𝐧o*, a sassy cutie bot 👻💕\n\n"
        "☑ Choose an option below:"
    )

    keyboard = [
        [InlineKeyboardButton("💬 Talk to 𝐀𝐤e𝐧o", callback_data="talk")],
        [
            InlineKeyboardButton("🧸 Friends", url="https://t.me/mich_family_group"),
            InlineKeyboardButton("🎮 Games", callback_data="games")
        ],
        [InlineKeyboardButton("👻 Meet me here", url="https://t.me/mich_family_group")],
        [InlineKeyboardButton("👥 Add me to your group", url="https://t.me/?startgroup=true")]
    ]

    try:
        await update.message.reply_photo(
            photo=BOT_IMAGE_URL,
            caption=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="MarkdownV2"  # safer for special characters and emojis
        )
    except Exception as e:
        print(f"❌ Error in start_command: {e}")

# Callback query handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return

    await query.answer()  # Always answer the callback first

    if query.data == "talk":
        await query.message.reply_text("Let's chat! 💬")

    elif query.data == "games":
        guide_text = (
            "💰 *Akeno Economy System Guide*\n\n"
            "💬 How it works:\n"
            "Manage your virtual money and items in the group! Use commands below to earn, gift, buy, or interact with others.\n\n"
            "🔨 *Economy Commands:*\n"
            "🔹 /close — Close economy commands working in the group\n"
            "🔹 /open — Open economy commands working in the group\n"
            "🔹 /bal — Check your/friend's balance\n"
            "🔹 /toprich — See top 10 richest users\n"
            "🔹 /topkill — See top 10 killers\n"
            "🔹 /give (Reply) amount — Gift money to someone\n"
            "🔹 /rob (Reply) amount (1-100000) — Rob someone\n"
            "🔹 /kill (Reply) — Kill someone\n"
            "🔹 /revive (Reply or without reply) — Revive you or your friend\n"
            "🔹 /protect 1d|2d — Buy protection\n"
            "🔹 /transfer amount — Owner only: Add/remove money\n\n"
            "🎁 *Item & Gifting*\n"
            "• Earn money by killing others\n"
            "• Gift money with 10% fee\n"
            "• Buy protection to avoid robbery\n"
            "• Top rankings for richest and killers"
        )
        await query.message.reply_text(guide_text, parse_mode="MarkdownV2")
