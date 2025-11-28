from telegram import Update, InputMediaAnimation
from telegram.ext import ContextTypes, CommandHandler
import random

# GIF URLs list (tumhe yaha apne slap GIFs ke links dalne honge)
SLAP_GIFS = [
    "https://media.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif",
    "https://media.giphy.com/media/jLeyZWgtwgr2U/giphy.gif",
]

async def slap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Command /slap ke saath reply me mention ya username
    if context.args:
        target = " ".join(context.args)
    elif update.message.reply_to_message:
        target = update.message.reply_to_message.from_user.first_name
    else:
        await update.message.reply_text("Kisko slap karna hai? 😏")
        return

    user = update.effective_user.first_name
    gif_url = random.choice(SLAP_GIFS)

    caption = f"{user} slapped {target} 👋"

    # Send GIF with caption
    await update.message.reply_animation(animation=gif_url, caption=caption)

# Add handler in main.py
# application.add_handler(CommandHandler("slap", slap))
