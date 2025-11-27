import random
import os
from datetime import datetime
from helpers import couples
from telegram import InputFile


async def couple(update, context):
    chat_id = update.effective_chat.id
    date = datetime.now().strftime("%Y-%m-%d")

    today_couple = couples.find_one({"chat_id": chat_id, "date": date})

    if today_couple:
        img = today_couple["img"]
        name1 = today_couple["p1"]
        name2 = today_couple["p2"]

        caption = (
            "💖 *Today's Cute Couple* 💖\n\n"
            f"{name1} ❤️ {name2}\n\n"
            "Love is in the air 💘\n\n"
            "~ From Shizu with love 💋"
        )

        return await update.message.reply_photo(
            photo=open(img, "rb"),
            caption=caption,
            parse_mode="Markdown"
        )

    members = await context.bot.get_chat_administrators(chat_id)
    users = [m.user for m in members]

    if len(users) < 2:
        return await update.message.reply_text("❌ Not enough users to pick a couple.")

    p1, p2 = random.sample(users, 2)
    name1 = p1.first_name
    name2 = p2.first_name

    folder = "assets/couple"
    imgs = os.listdir(folder)
    img = os.path.join(folder, random.choice(imgs))

    couples.insert_one({
        "chat_id": chat_id,
        "date": date,
        "p1": name1,
        "p2": name2,
        "img": img
    })

    caption = (
        "💖 *Today's Cute Couple* 💖\n\n"
        f"{name1} ❤️ {name2}\n\n"
        "Love is in the air 💘\n\n"
        "~ From Shizu with love 💋"
    )

    await update.message.reply_photo(
        photo=open(img, "rb"),
        caption=caption,
        parse_mode="Markdown"
    )
