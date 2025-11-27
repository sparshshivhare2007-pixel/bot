import random
from telegram import Update
from telegram.ext import ContextTypes

# Minimal working couple command
async def couple(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Try to get some members (just sender for now)
    members = [update.effective_user]

    # Check if enough members
    if len(members) < 2:
        # Duplicate sender to make 2 for demo
        members = members * 2

    # Pick 2 random members
    p1, p2 = random.sample(members, 2)
    name1 = p1.first_name
    name2 = p2.first_name

    # Send result
    caption = (
        f"💖 *Today's Cute Couple* 💖\n\n"
        f"{name1} ❤️ {name2}\n\n"
        "Love is in the air 💘\n\n"
        "~ From Shizu with love 💋"
    )

    await update.message.reply_text(caption, parse_mode="Markdown")
