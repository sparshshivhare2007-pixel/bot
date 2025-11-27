from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ApplicationBuilder

# 🚨 IMPORTANT: Replace this URL with the direct link to your bot's welcome image.
# यहाँ अपनी Kiddo/Akeno इमेज की वास्तविक लिंक डालें।
# Note: I am using a generic placeholder as I cannot access the new image link directly.
BOT_IMAGE_URL = "https://files.catbox.moe/z1skp4.jpg" 

# /start command
async def start_command(update: Update, context: CallbackContext):
    user = update.effective_user

    # The text remains the same, but will now be used as the photo's caption.
    # Note: I am keeping 'Akeno' as per previous context, assuming you want that name.
    text = (
        f"👋 Hey, →🪬{user.first_name}🪬🤍\n"
        "💞 You're talking to *𝐀𝐤e𝐧o*, a sassy cutie bot 👻💕\n\n"
        "☑ Choose an option below:"
    )

    keyboard = [
        # 1. Talk button
        [InlineKeyboardButton("💬 Talk to 𝐀𝐤e𝐧o", callback_data="talk")],
        
        # 2. Friends and Games (on the same row)
        [
            InlineKeyboardButton("🧸 Friends", url="https://t.me/mich_family_group"),
            InlineKeyboardButton("🎮 Games", callback_data="games")
        ],
        
        # 3. New 'Meet me here' button (assuming this is a chat link)
        [InlineKeyboardButton("👻 Meet me here", url="https://t.me/mich_family_group")], 
        
        # 4. Add me to group button
        [InlineKeyboardButton("👥 Add me to your group", url="https://t.me/?startgroup=true")]
    ]

    # Use reply_photo to send the image.
    await update.message.reply_photo(
        photo=BOT_IMAGE_URL,
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Callback query handler
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    
    game_features_text = (
        "🎮 Game Features\n\n"
        "To know about the Lottery System, tap /game\n"
        "To know about the Economy System, tap /economy\n\n"
        "Have fun and be lucky 🍀"
    )

    if query.data == "talk":
        await query.answer() 
        await query.message.reply_text("Let's chat! 💬")
        
    elif query.data == "games":
        await query.answer(
            text=game_features_text, 
            show_alert=True 
        )
