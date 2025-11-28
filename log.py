import os

from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import ContextTypes

from pymongo import MongoClient

from dotenv import load_dotenv

# Load configuration and MongoDB client from main environment

load_dotenv()

# Note: OWNER_ID and MONGO_URI must be in the .env file

MONGO_URI = os.getenv("MONGO_URI")

# Use a default value of 0 in case OWNER_ID is missing or not an integer

OWNER_ID = int(os.getenv("OWNER_ID", 0)) 

# --- MongoDB Setup ---

client = MongoClient(MONGO_URI)

db = client["economy_bot"]

settings = db["settings"] # Collection to store log chat ID

# --- Helper Functions ---

def get_log_chat_id():

    """Retrieves the log chat ID from MongoDB settings."""

    log_setting = settings.find_one({"_id": "log_chat"})

    # Returns the chat ID or None if not set

    return log_setting.get("chat_id") if log_setting else None

def is_owner(user_id):

    """Checks if the user ID matches the defined OWNER_ID."""

    return user_id == OWNER_ID

# --- Core Logging Sender ---

async def send_log_message(bot: Bot, text: str, parse_mode='HTML'):

    """Sends the log message to the configured log chat or the owner's DM."""

    log_chat_id = get_log_chat_id()

    target_id = log_chat_id if log_chat_id else OWNER_ID

    if target_id:

        try:

            # For logging, we must use context.bot which is a Bot instance

            await bot.send_message(chat_id=target_id, text=text, parse_mode=parse_mode)

        except Exception as e:

            print(f"Error sending log message to {target_id}: {e}")

    else:

        print("Warning: Log chat ID and OWNER_ID are not set. Cannot send logs.")

# 1. Bot Startup Log Message

async def log_bot_startup(bot: Bot, total_users: int):

    """Sends a log message when the bot starts."""

    

    owner_info = await bot.get_chat(OWNER_ID)

    owner_name = owner_info.first_name

    owner_username = f"@{owner_info.username}" if owner_info.username else "@No Username"

    message = (

        f"𝐊𝐚𝐦𝐚𝐥 ʜᴀs sᴛᴀʀᴛᴇᴅ ʙᴏᴛ.\n\n"

        f"ɴᴀᴍᴇ : {owner_name}\n"

        f"ᴜsᴇʀɴᴀᴍᴇ : {owner_username}\n"

        f"ɪᴅ : <code>{OWNER_ID}</code>\n\n"

        f"ᴛᴏᴛᴀʟ ᴜsᴇʀs : {total_users}"

    )

    await send_log_message(bot, message, parse_mode='HTML')

# 2. Bot Added to Group Log Message

async def log_bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """Sends a log message when the bot is added to a new group."""

    

    # Check if the bot was the member added

    for member in update.message.new_chat_members:

        if member.id == context.bot.id:

            break

    else:

        return # Bot was not the member added

    chat = update.effective_chat

    added_by = update.effective_user

    

    # Get group details

    chat_id = chat.id

    chat_name = chat.title

    

    # Try to get invite link

    invite_link = "No Link"

    try:

        if chat.type in ["group", "supergroup"]:

            export_link = await context.bot.export_chat_invite_link(chat_id)

            invite_link = export_link if export_link else "Private Group/No Export Permission"

    except Exception:

        invite_link = "No Link (Bot Admin rights required)"

    # Get member count (approximate)

    member_count = "Unknown"

    try:

        member_count = await context.bot.get_chat_member_count(chat_id)

    except Exception:

        pass

        

    # Get total chat count (Assuming 'groups' collection tracks all chats the bot is in)

    total_chats = settings.find_one({"_id": "chat_count"})

    # Increment count for the log message, then update DB

    total_chats_count = total_chats.get("count", 0) + 1 

    

    # Construct log message

    message = (

        f"📝𝐁ᴏᴛ 𝐀ᴅᴅᴇᴅ 𝐈ɴ 𝐀 #𝐍ᴇᴡ_𝐆ʀᴏᴜᴘ\n\n"

        f"📌𝐂ʜᴀᴛ 𝐍ᴀᴍᴇ: {chat_name}\n"

        f"🍂𝐂ʜᴀᴛ 𝐈ᴅ: <code>{chat_id}</code>\n"

        f"🔐𝐂ʜᴀᴛ 𝐔sᴇʀɴᴀᴍᴇ: @{chat.username if chat.username else '𝐏ʀɪᴠᴀᴛᴇ 𝐆ʀᴏᴜᴘ'}\n"

        f"🖇️𝐆ʀᴏ𝐮𝐩 𝐋ɪɴᴋ: {invite_link}\n"

        f"📈𝐆ʀᴏ𝐮𝐩 𝐌ᴇᴍʙᴇʀs: {member_count}\n"

        f"🤔𝐀ᴅᴅᴇᴅ 𝐁ʏ: {added_by.first_name} (<a href='tg://user?id={added_by.id}'>{added_by.first_name}</a>)\n\n"

        f"ᴛᴏᴛᴀʟ ᴄʜᴀᴛs : {total_chats_count}"

    )

    

    # Update total chat count in MongoDB

    settings.update_one({"_id": "chat_count"}, {"$inc": {"count": 1}}, upsert=True)

    

    await send_log_message(context.bot, message, parse_mode='HTML')

# 3. Bot Removed from Group Log Message

async def log_bot_removed(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """Sends a log message when the bot is removed from a group."""

    

    chat = update.effective_chat

    remover = update.effective_user

    

    chat_id = chat.id

    chat_name = chat.title

    chat_username = chat.username if chat.username else "𝐏ʀɪᴠᴀᴛᴇ 𝐂ʜᴀᴛ"

    

    # Construct log message

    message = (

        f"𝐈 𝐥𝐞𝐟𝐭 𝐟𝐫𝐨𝐦 𝐚 𝐠𝐫𝐨𝐮𝐩:-\n\n"

        f"𝐍𝐚𝐦𝐞:- {chat_name}\n"

        f"𝐈𝐃:- <code>{chat_id}</code>\n"

        f"𝐔_𝐍𝐀𝐌𝐄:- {chat_username}\n\n"

        # The mention is crucial here:

        f"𝐁𝐘:- <a href='tg://user?id={remover.id}'>♡⃝ {remover.first_name}</a>" 

    )

    

    # Update total chat count (decrement)

    settings.update_one({"_id": "chat_count"}, {"$inc": {"count": -1}}, upsert=True)

    

    await send_log_message(context.bot, message, parse_mode='HTML')

# --- Owner Commands for Log Settings ---

async def setlog(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """Sets the current chat as the log chat (Owner only)."""

    user_id = update.effective_user.id

    if not is_owner(user_id):

        return await update.message.reply_text("❌ This command is owner only!")

        

    chat_id = update.effective_chat.id

    

    # Store log chat ID in settings collection

    settings.update_one(

        {"_id": "log_chat"},

        {"$set": {"chat_id": chat_id}},

        upsert=True

    )

    await update.message.reply_text(

        f"✅ Log chat set successfully!\n"

        f"All bot activity will now be sent here (Chat ID: <code>{chat_id}</code>).",

        parse_mode='HTML'

    )

async def dellog(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """Deletes the log chat setting (Owner only)."""

    user_id = update.effective_user.id

    if not is_owner(user_id):

        return await update.message.reply_text("❌ This command is owner only!")

        

    # Remove log chat ID from settings collection

    settings.delete_one({"_id": "log_chat"})

    await update.message.reply_text(

        "🗑️ Log chat setting deleted. Log messages will now be sent to the owner's DM.",

        parse_mode='HTML'

    )

