from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# ---- Your Channel Link ----
CHANNEL_LINK = "https://t.me/mich_family_group"

# ---- Welcome Image URL ----
BOT_IMAGE_URL = "https://files.catbox.moe/z1skp4.jpg"


# ===================== /start COMMAND =====================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    buttons = [
        [InlineKeyboardButton("✦ Talk to Akeno 💬", callback_data="talk")],
        [
            InlineKeyboardButton("✦ Friends 🧸", callback_data="friends"),
            InlineKeyboardButton("✦ Games 🎮", callback_data="games")
        ],
        [InlineKeyboardButton("✦ Add me to your group 👫", url=f"https://t.me/{context.bot.username}?startgroup=true")]
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    caption = (
        f"✨ Hey <a href='tg://user?id={user.id}'>{user.first_name}</a> ~ 🌹\n\n"
        f"◎ You're talking to Baka, a sassy cute bot 💕\n"
        f"✦ Choose an option below:"
    )

    if update.message:
        await update.message.reply_photo(
            photo=BOT_IMAGE_URL,
            caption=caption,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    else:
        await update.callback_query.message.reply_photo(
            photo=BOT_IMAGE_URL,
            caption=caption,
            reply_markup=keyboard,
            parse_mode="HTML"
        )


# ===================== BUTTON HANDLER =====================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # ---- TALK BUTTON ----
    if query.data == "talk":
        await query.edit_message_text("💬 Talking feature coming soon!")

    # ---- FRIENDS BUTTON ----
    elif query.data == "friends":
        await query.edit_message_text(
            f"🧸 Join our family community:\n👉 {CHANNEL_LINK}"
        )

    # ---- GAMES BUTTON (Economy Guide) ----
    elif query.data == "games":
        await query.edit_message_text("🎮 Sending the Economy Guide...")

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
