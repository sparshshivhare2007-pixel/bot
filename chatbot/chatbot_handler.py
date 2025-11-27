from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from chatbot.gemini_client import ask_gemini  # Gemini API call

# Personality wrapper
def personality_wrap(text: str) -> str:
    """Adds Shizuka style prefix/suffix + emojis to AI reply."""
    # You can make this fancier later with random phrases
    return f"🌸 Shizuka says: {text} 🌼"

async def chatbot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    full_text = update.message.text
    bot_username = context.bot.username
    prompt = ""

    # Group Chat Logic
    if update.effective_chat.type in ["group", "supergroup"]:
        mention_tag = f"@{bot_username}"
        if full_text.startswith(mention_tag):
            prompt = full_text[len(mention_tag):].strip()
        elif update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
            prompt = full_text
        else:
            return
    else:
        prompt = full_text  # private chat

    if not prompt:
        return

    # Typing animation
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # AI response
    response_text = await ask_gemini(prompt)

    # Personality + emoji wrap
    final_reply = personality_wrap(response_text)

    await update.message.reply_text(final_reply)
