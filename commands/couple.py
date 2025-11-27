import random
from telegram import Update
from telegram.ext import ContextTypes

# Minimal couple command
async def couple(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Get at least 2 users: just the sender and the bot itself for demo
    members = [update.effective_user]

    if len(members) < 2:
        return await update.message.reply_text("❌ Not enough users to select a couple!")

    # Pick random couple (in this minimal case, same user twice)
    p1, p2 = random.sample(members * 2, 2)  # duplicate to ensure 2
    name1 = p1.first_name
    name2 = p2.first_name

    caption = (
        "💖 *Today's Cute Couple* 💖\n\n"
        f"{name1} ❤️ {name2}\n\n"
        "Love is in the air 💘\n\n"
        "~ From Shizu with love 💋"
    )

    await update.message.reply_text(caption, parse_mode="Markdown")
