import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import LOG_GROUP_ID, OWNER_ID
from MyGameBot import app  # aapke bot instance
from MyGameBot.utils.database import (
    add_served_chat,
    delete_served_chat,
    get_assistant,
    add_user_balance,
    get_total_users,
    get_total_groups
)

# ----------------- Media -----------------
welcome_photo = "https://files.catbox.moe/ajobub.jpg"
leave_photos = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg",
    "https://telegra.ph/file/a7d663cd2de689b811729.jpg",
]

# ----------------- Bot Added To Group -----------------
@app.on_message(filters.new_chat_members, group=-10)
async def join_watcher(_, message: Message):
    try:
        userbot = await get_assistant(message.chat.id)
        chat = message.chat

        for member in message.new_chat_members:
            if member.id == app.id:  # Bot added
                count = await app.get_chat_members_count(chat.id)
                username = chat.username if chat.username else "Private Group"

                # Optional invite link
                invite_link = ""
                try:
                    if not chat.username:
                        link = await app.export_chat_invite_link(chat.id)
                        invite_link = f"\nGroup Link: {link}" if link else ""
                except:
                    pass

                # Log bot added
                msg = (
                    f"🎮 Game Bot Added 🎮\n\n"
                    f"Chat Name: {chat.title}\n"
                    f"Chat ID: {chat.id}\n"
                    f"Username: @{username}\n"
                    f"Total Members: {count}\n"
                    f"Added By: {message.from_user.mention if message.from_user else 'Unknown'}"
                    f"{invite_link}"
                )
                buttons = []
                if message.from_user:
                    buttons.append([InlineKeyboardButton("Added By", url=f"tg://openmessage?user_id={message.from_user.id}")])
                await app.send_photo(LOG_GROUP_ID, photo=welcome_photo, caption=msg, reply_markup=InlineKeyboardMarkup(buttons) if buttons else None)

                # Add group to DB
                await add_served_chat(message.chat.id)
                if username:
                    await userbot.join_chat(f"@{username}")

                # Optional: send bot intro in group
                await app.send_message(chat.id, "🎉 I’m your Economy Bot! Type /start to begin.")

    except Exception as e:
        print(f"Error in join_watcher: {e}")


# ----------------- Bot Removed From Group -----------------
@app.on_message(filters.left_chat_member, group=-12)
async def left_watcher(_, message: Message):
    try:
        userbot = await get_assistant(message.chat.id)
        left_member = message.left_chat_member

        if left_member and left_member.id == (await app.get_me()).id:
            removed_by = message.from_user.mention if message.from_user else "Unknown User"
            chat_title = message.chat.title
            chat_username = f"@{message.chat.username}" if message.chat.username else "Private Chat"
            chat_id = message.chat.id

            caption = (
                f"❌ Game Bot Removed ❌\n\n"
                f"Chat Name: {chat_title}\n"
                f"Chat ID: {chat_id}\n"
                f"Removed By: {removed_by}\n"
                f"Bot: @{app.username}"
            )
            await app.send_photo(LOG_GROUP_ID, photo=random.choice(leave_photos), caption=caption)

            # Remove group from DB
            await delete_served_chat(chat_id)
            await userbot.leave_chat(chat_id)

    except Exception as e:
        print(f"Error in left_watcher: {e}")


# ----------------- Welcome New Member in Group -----------------
@app.on_message(filters.new_chat_members)
async def welcome_new_member(_, message: Message):
    for member in message.new_chat_members:
        if member.id != (await app.get_me()).id:
            await add_user_balance(member.id, 50)  # small starting balance
            await message.reply(f"🎉 Welcome {member.mention}!\n💰 You received 50 coins to start playing!\nUse /balance to check your money.")


# ----------------- /status Command (Owner Only) -----------------
@app.on_message(filters.command("status") & filters.user(OWNER_ID))
async def status(_, message: Message):
    total_groups = await get_total_groups()
    total_users = await get_total_users()
    await message.reply(f"📊 Bot Status:\n\nTotal Groups: {total_groups}\nTotal Users: {total_users}")
