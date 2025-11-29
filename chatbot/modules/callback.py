from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from pyrogram.enums import ChatMemberStatus as CMS
from chatbot import ChatBot
from chatbot.database import db

vick = db["VickDb"]["Vick"]  # Chatbot-specific collection

@ChatBot.on_callback_query()
async def cb_handler(_, query: CallbackQuery):
    # Example: adding/removing chat from chatbot
    if query.data == "addchat":
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in [CMS.OWNER, CMS.ADMINISTRATOR]:
            return await query.answer("You're not admin!", show_alert=True)
        if vick.find_one({"chat_id": query.message.chat.id}):
            vick.delete_one({"chat_id": query.message.chat.id})
            await query.edit_message_text(f"Chatbot enabled by {query.from_user.mention}.")
        else:
            await query.edit_message_text("Chatbot already enabled.")

    elif query.data == "rmchat":
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in [CMS.OWNER, CMS.ADMINISTRATOR]:
            return await query.answer("You're not admin!", show_alert=True)
        if not vick.find_one({"chat_id": query.message.chat.id}):
            vick.insert_one({"chat_id": query.message.chat.id})
            await query.edit_message_text(f"Chatbot disabled by {query.from_user.mention}.")
        else:
            await query.edit_message_text("Chatbot already disabled.")
