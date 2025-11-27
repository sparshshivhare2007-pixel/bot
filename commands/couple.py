import random
import os
from datetime import datetime
from helpers import couples   # <-- New MongoDB collection
from telegram import InputFile


async def couple(update, context):
    chat_id = update.effective_chat.id
    date = datetime.now().strftime("%Y-%m-%d")

    # 1) Check if couple for today already exists
    today_couple = couples.find_one({"chat_id": chat_id, "date": date})

    if today_couple:
        # Already selected → show same couple
        img = today_couple["img"]
        p1 = today_couple["p1"]
        p2 = today_couple["p2"]

        return await update.message.reply_photo(
            photo=open(img, "rb"),
            caption=f"💘 *Today's Couple:*\n\n❤️ {p1} + {p2} ❤️",
            parse_mode="Markdown"
        )

    # 2) Get all chat members
    members = await context.bot.get_chat_administrators(chat_id)
    users = [m.user for m in members]

    if len(users) < 2:
        return await update.message.reply_text("❌ Not enough users to pick a couple.")

    # 3) Random pair
    p1, p2 = random.sample(users, 2)
    name1 = p1.first_name
    name2 = p2.first_name

    # 4) Random couple image from folder
    folder = "assets/couple"
    imgs = os.listdir(folder)
    img = os.path.join(folder, random.choice(imgs))

    # 5) Save to MongoDB
    couples.insert_one({
        "chat_id": chat_id,
        "date": date,
        "p1": name1,
        "p2": name2,
        "img": img
    })

    # 6) Send result
    await update.message.reply_photo(
        photo=open(img, "rb"),
        caption=f"💘 *Couple of the Day*\n\n❤️ {name1} + {name2} ❤️",
        parse_mode="Markdown"
    )
