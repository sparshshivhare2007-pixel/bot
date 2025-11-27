from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from chatbot.gemini_client import ask_gemini  # Gemini API call

async def chatbot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles non-command text messages.
    Shows typing animation while waiting for AI response.
    """

    full_text = update.message.text
    bot_username = context.bot.username
    prompt = ""

    # Group Chat Logic: only respond if mentioned or replied to bot
    if update.effective_chat.type in ["group", "supergroup"]:
        mention_tag = f"@{bot_username}"
        if full_text.startswith(mention_tag):
            prompt = full_text[len(mention_tag):].strip()
        elif update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
            prompt = full_text
        else:
            return  # ignore messages not for bot
    else:
        # Private chat: respond to all messages
        prompt = full_text

    if not prompt:
        return

    # -------------------- Typing Animation --------------------
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # Call Gemini API
    response_text = await as_
