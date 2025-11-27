import random
import os
from datetime import datetime
from helpers import couples
from telegram.constants import ChatMemberStatus  # fixed



async def couple(update, context):
    chat_id = update.effective_chat.id
    date = datetime.now().strftime("%Y-%m-%d")

    # ---- Step 1: Check if saved result exists ----
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

    # ---- Step 2: Get group members safely ----
    members = []
    try:
        member_list = await context.bot.get_chat_administrators(chat_id)
        # Add admins
        for m in member_list:
            members.append(m.user)
    except:
        pass

    # Add sender at least
    if update.effective_user not in members:
        members.append(update.effective_user)

    # If still too few
    if len(members) < 2:
        return await update.message.reply_text("❌ Not enough users to select a couple!")

    # ---- Step 3: Pick random couple ----
    p1, p2 = random.sample(members, 2)
    name1 = p1.first_name
    name2 = p2.first_name

    # ---- Step 4: Choose random image ----
    folder = "assets/couple"
    imgs = os.listdir(folder)
    img = os.path.join(folder, random.choice(imgs))

    # ---- Step 5: Save to DB ----
    couples.insert_one({
        "chat_id": chat_id,
        "date": date,
        "p1": name1,
        "p2": name2,
        "img": img
    })

    # ---- Step 6: Send result ----
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
