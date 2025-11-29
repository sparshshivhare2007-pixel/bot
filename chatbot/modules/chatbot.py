import random
from pymongo import MongoClient
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from chatbot import ChatBot
from config import MONGO_URL

chat_previous_messages = {}

def get_random_database_reply(chatai):
    try:
        all_replies = list(chatai.find({}))
        if all_replies:
            chosen = random.choice(all_replies)
            return chosen["text"], chosen.get("check", "none")
        return None, None
    except:
        return None, None

@ChatBot.on_message((filters.text | filters.sticker | filters.group) & ~filters.private & ~filters.bot)
async def chatbot_universal(client: Client, message: Message):
    global chat_previous_messages

    # Skip commands
    if message.text and message.text[0] in "!/?@#":
        return

    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]
    vickdb = MongoClient(MONGO_URL)
    vick = vickdb["VickDb"]["Vick"]
    is_vick = vick.find_one({"chat_id": message.chat.id})
    chat_id = message.chat.id

    # Learning
    if message.reply_to_message:
        word = message.reply_to_message.text if message.reply_to_message.text else getattr(message.reply_to_message.sticker, "file_unique_id", None)
        reply_text = message.text if message.text else getattr(message.sticker, "file_id", None)
        reply_check = "sticker" if message.sticker else "none"
        if word and reply_text:
            if not chatai.find_one({"word": word, "text": reply_text}):
                chatai.insert_one({"word": word, "text": reply_text, "check": reply_check})
    else:
        prev_msg = chat_previous_messages.get(chat_id)
        if prev_msg:
            word = prev_msg["content"]
            reply_text = message.text if message.text else getattr(message.sticker, "file_id", None)
            reply_check = "sticker" if message.sticker else "none"
            if word and reply_text:
                if not chatai.find_one({"word": word, "text": reply_text}):
                    chatai.insert_one({"word": word, "text": reply_text, "check": reply_check})

    # Store current message
    chat_previous_messages[chat_id] = {"type": "sticker" if message.sticker else "text", "content": message.sticker.file_unique_id if message.sticker else message.text, "user_id": message.from_user.id}

    # Respond only if chatbot is enabled
    if not is_vick:
        should_respond = False
        search_word = message.text if message.text else getattr(message.sticker, "file_unique_id", None)
        if search_word:
            # Random 10% chance in group for text
            if message.text and random.randint(1, 10) == 1:
                should_respond = True
            # Random 5% chance for sticker
            elif message.sticker and random.randint(1, 20) == 1:
                should_respond = True
        if should_respond:
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            responses = list(chatai.find({"word": search_word}))
            if responses:
                reply = random.choice(responses)
                reply_data = chatai.find_one({"word": search_word, "text": reply["text"]})
                try:
                    if reply_data and reply_data.get("check") == "sticker":
                        await message.reply_sticker(reply["text"])
                    else:
                        await message.reply_text(reply["text"])
                except:
                    await message.reply_text(reply["text"])
            else:
                rand_reply, check_type = get_random_database_reply(chatai)
                if rand_reply:
                    try:
                        if check_type == "sticker":
                            await message.reply_sticker(rand_reply)
                        else:
                            await message.reply_text(rand_reply)
                    except:
                        await message.reply_text(rand_reply)
