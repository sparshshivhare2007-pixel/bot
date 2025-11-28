from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# IMAGE FOR GROUP START
BOT_IMAGE_URL = "https://files.catbox.moe/z1skp4.jpg"
STICKER_ID = "`CAACAgQAAxkBAAEPiQppKcATJi3RB9_QwVlyK2EjxisdogACUhUAAnRkqVPXj4u7QSZIGR4E`"  # apna DM sticker id


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    # CLICKABLE NAME
    mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

    # ---------- DM START ----------
    if chat.type == "private":
        # DM style
        text = (
            f"Welcome Baby 🩵\n"
            f"{mention} <i>🌹</i>\n"
            f".. 😅"
        )

        # send sticker first
        await update.message.reply_sticker(STICKER_ID)

        # send DM message
        await update.message.reply_text(
            text,
            parse_mode="HTML"
        )
        return

    # ---------- GROUP START ----------
    # Group style (image + buttons)
    text = (
        f"👋 Hey, →🪬{mention}🪬🤍\n"
        "💞 You're talking to <b>𝐀𝐤e𝐧o</b>, a sassy cutie bot 👻💕\n\n"
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

    await update.message.reply_photo(
        photo=BOT_IMAGE_URL,
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


# Callback query handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "talk":
        await query.message.reply_text("Let's chat! 💬")

    elif query.data == "games":
        await query.message.reply_text(
            "💰 <b>Akeno Economy System Guide</b>\n\n"
            "💬 How it works:\n"
            "Manage your virtual money and items in the group! Use commands below to earn, gift, buy, or interact with others.\n\n"
            "🔨 <b>Economy Commands:</b>\n"
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
            "🎁 <b>Item & Gifting</b>\n"
            "• Earn money by killing others\n"
            "• Gift money with 10% fee\n"
            "• Buy protection to avoid robbery\n"
            "• Top rankings for richest and killers",
            parse_mode="HTML"
        )
