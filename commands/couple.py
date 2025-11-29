from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import random
import time
import os
from helpers import get_user  # helpers ke hisaab se

# ----------------- BASE DIRECTORY -----------------
# couple.py is in 'commands' folder, GIFs are in 'gifs' folder at root
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # go one level up from commands/

# ----------------- YOUR COUPLE GIFS -----------------
COUPLE_GIFS = [
    os.path.join(BASE_DIR, "gifs/meri_couple.gif"),
    os.path.join(BASE_DIR, "gifs/dusri_couple.gif"),
    os.path.join(BASE_DIR, "gifs/teesri_couple.gif")
]

# Couples storage: key = (user1_id, user2_id), value = timestamp
couples = {}

# Clean expired couples (older than 24 hours)
def clean_expired_couples():
    now = time.time()
    expired = [pair for pair, ts in couples.items() if now - ts > 86400]
    for pair in expired:
        del couples[pair]

# ----------------- MAIN COUPLE COMMAND -----------------
async def couple(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clean_expired_couples()
    chat = update.effective_chat

    # Fetch all members (admins + sender)
    members = []
    try:
        admins = await context.bot.get_chat_administrators(chat.id)
        for admin in admins:
            if not admin.user.is_bot:
                members.append(admin.user)

        # Add message sender if not already in members
        user = update.effective_user
        if user not in members and not user.is_bot:
            members.append(user)

    except Exception:
        await update.message.reply_text(
            "⚠️ Bot needs to be admin or cannot fetch members 😅"
        )
        return

    if len(members) < 2:
        await update.message.reply_text("Group me kam se kam 2 members hone chahiye 😅")
        return

    # Pick a random couple not already used
    attempts = 0
    max_attempts = 50
    while attempts < max_attempts:
        user1, user2 = random.sample(members, 2)
        pair_key = tuple(sorted([user1.id, user2.id]))
        if pair_key not in couples:
            couples[pair_key] = time.time()
            break
        attempts += 1
    else:
        # Pick random existing couple if all pairs exist
        pair_key = random.choice(list(couples.keys()))
        user1 = next(u for u in members if u.id == pair_key[0])
        user2 = next(u for u in members if u.id == pair_key[1])
        couples[pair_key] = time.time()  # refresh timestamp

    # Pick random GIF
    gif_file = random.choice(COUPLE_GIFS)

    # Caption
    caption = (
        f"💑 𝑻𝒐𝒅𝒂𝒚'𝒔 𝒄𝒐𝒖𝒑𝒍𝒆 💑\n\n"
        f"<b><a href='tg://user?id={user1.id}'>{user1.first_name}</a></b> 💖 "
        f"<b><a href='tg://user?id={user2.id}'>{user2.first_name}</a></b>\n\n"
        f"Today's couple! 🔥"
    )

    # Send animation safely
    try:
        with open(gif_file, "rb") as f:
            await update.message.reply_animation(
                animation=f,
                caption=caption,
                parse_mode="HTML"
            )
    except FileNotFoundError:
        await update.message.reply_text(
            "❌ GIF file nahi mili. Please check the filename/path."
        )
