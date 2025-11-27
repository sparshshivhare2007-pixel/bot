import os, random
from telegram import Update
from telegram.ext import ContextTypes

ASSETS_PATH = "assets"

async def hug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /hug @username")
        return

    target = " ".join(context.args)
    message = f"🤗 {update.effective_user.first_name} sent a hug to {target}!"
    await update.message.reply_text(message)

    # Random video from hug folder
    hug_videos = os.listdir(os.path.join(ASSETS_PATH, "gifs", "hug"))
    video_file = os.path.join(ASSETS_PATH, "gifs", "hug", random.choice(hug_videos))

    await update.message.reply_video(video=open(video_file, "rb"))
