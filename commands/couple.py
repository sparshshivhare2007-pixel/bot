import random
import os
from datetime import datetime
from helpers import couples


async def couple(update, context):
    chat_id = update.effective_chat.id
    date = datetime.now().strftime("%Y-%m-%d")

    # 1. Check today's saved couple
    today = couples.find_one({"chat_id": chat_id, "date": date})
    if today:
        img = today["img"]
        name1 = today["p1"]
        name2 = today["p2"]

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

    # 2. Select random users from chat (using message history)
    users = []

    async for msg in context.bot.get_chat_history(chat_id, limit=50):
        if msg.from_user and msg.from_user.id not in [u.id for u in users]:
            users.append(msg.from_user)

    if len(users) < 2:
        return await update.message.reply_text("❌ Not enough users to create a couple.")

    # 3. Pick randomly
    p1, p2 = random.sample(users, 2)
    name1, name2 = p1.first_name, p2.first_name

    # 4. Random image
    folder = "assets/couple"
    imgs = os.listdir(folder)
    img = os.path.join(folder, random.choice(imgs))

    # 5. Save to DB
    couples.insert_one({
        "chat_id": chat_id,
        "date": date,
        "p1": name1,
        "p2": name2,
        "img": img
    })

    # 6. Send result
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
