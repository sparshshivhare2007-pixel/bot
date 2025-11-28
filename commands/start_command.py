# start_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# 🚨 IMPORTANT: Replace this URL with the direct link to your bot's welcome image
BOT_IMAGE_URL = "https://files.catbox.moe/z1skp4.jpg"

# /start command
async def start_command(update: Update, context: CallbackContext):
    user = update.effective_user

    text = (
    f"⬤ 𖦹 {user.first_name} - ᴄᴜᴛɪᴇ, ꜱᴀꜱꜱʏ, ᴀ ʟɪᴛᴛʟᴇ ᴡɪʟᴅ ᴀɴᴅ ɢᴀᴍᴇ ᴘᴀʀᴛɴᴇʀ 🤍\n\n"
    "⬤ ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴇɴᴊᴏʏ ᴛʜᴇ ᴄʜᴀᴛꜱ ᴀɴᴅ ɢᴀᴍᴇꜱ ᴡɪᴛʜ ᴍᴇ ᴛʜᴀᴛ ᴍᴀᴋᴇꜱ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴡɪʟʟ ʙᴇ ᴍᴏꜱᴛ ᴀᴄᴛɪᴠᴇ!\n\n"
    "☑ Choose an option below:"
        
    )

    
keyboard = [
    [InlineKeyboardButton("💬 Talk to 𝐀𝐤e𝐧o", callback_data="talk")],
    [
        InlineKeyboardButton("🧸 Friends", url="https://t.me/mich_family_group"),
        InlineKeyboardButton("🎮 Games", callback_data="games")
    ],
    [InlineKeyboardButton("👻 Meet me here", url="https://t.me/mich_family_group")],
    [InlineKeyboardButton("👥 Add me to your group", url="https://t.me/?startgroup=true")],
    [InlineKeyboardButton("🔑 Owner Panel", url="https://t.me/INTROVERT_HU_YRR")]  # 🔥 CLICKABLE OWNER BUTTON 
]


    await update.message.reply_photo(
        photo=BOT_IMAGE_URL,
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Callback query handler
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query

    if query.data == "talk":
        await query.answer()
        await query.message.reply_text("Let's chat! 💬")

    elif query.data == "games":
        await query.answer()
        await query.message.reply_text(
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
            "• Top rankings for richest and killers",
            parse_mode="Markdown"
        )
