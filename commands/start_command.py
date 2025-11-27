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
            # Friends button opens URL directly
            InlineKeyboardButton("🧸 Friends", url="https://t.me/mich_family_group"),
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
    
    # Text for the Game Features pop-up alert
    game_features_text = (
        "🎮 Game Features\n\n"
        "To know about the Lottery System, tap /game\n"
        "To know about the Economy System, tap /economy\n\n"
        "Have fun and be lucky 🍀"
    )

    if query.data == "talk":
        await query.answer() # Acknowledge the press
        await query.message.reply_text("Let's chat! 💬")
        
    elif query.data == "games":
        # Send a pop-up alert (modal) with game features
        await query.answer(
            text=game_features_text, 
            show_alert=True 
        )
        
    # 'friends' is handled by URL and does not need an 'elif' block here.
