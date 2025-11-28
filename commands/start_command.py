from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

CHANNEL_LINK = "https://t.me/mich_family_group"

# ---------------- BUTTON HANDLER ----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # TALK
    if query.data == "talk":
        await query.message.chat.send_message("💬 Talking feature coming soon!")

    # FRIENDS
    elif query.data == "friends":
        await query.message.chat.send_message(
            f"🧸 Join our family community:\n👉 {CHANNEL_LINK}"
        )

    # GAMES → Economy Guide
    elif query.data == "games":

        guide_text = (
            "💰 *Economy Game Guide*\n"
            "Here are your full economy commands:\n\n"

            "🔨 *Economy Commands:*\n"
            "🔹 `/close` — Close economy commands working in the group\n"
            "🔹 `/open` — Open economy commands working in the group\n"
            "🔹 `/bal` — Check your/friend's balance\n"
            "🔹 `/toprich` — See top 10 richest users\n"
            "🔹 `/topkill` — See top 10 killers\n"
            "🔹 `/give` (Reply) `amount` — Gift money\n"
            "🔹 `/rob` (Reply) `amount` — Rob someone\n"
            "🔹 `/kill` (Reply) — Kill someone\n"
            "🔹 `/revive` — Revive yourself or a friend\n"
            "🔹 `/protect 1d|2d` — Buy protection\n"
            "🔹 `/transfer amount` — Owner only: Add/remove money\n\n"

            "🎁 *Item & Gifting*\n"
            "• Earn money by killing others\n"
            "• Gift money with 10% fee\n"
            "• Buy protection to avoid robbery\n"
            "• Top rankings for richest and killers\n\n"

            "✨ *Aur bhi economy commands coming soon...*"
        )

        await query.message.chat.send_message(
            guide_text,
            parse_mode="Markdown"
        )

# ---------------- START COMMAND ----------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🗣 Talk", callback_data="talk"),
            InlineKeyboardButton("👥 Friends", callback_data="friends"),
        ],
        [
            InlineKeyboardButton("🎮 Games", callback_data="games"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo="https://files.catbox.moe/z1skp4.jpg",
        caption="👋 Welcome!",
        reply_markup=reply_markup
    )
