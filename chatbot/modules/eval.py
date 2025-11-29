import asyncio
import traceback
import sys
from io import StringIO
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from chatbot import ChatBot, OWNER

def is_dev_filter():
    return filters.user(OWNER)

async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    await func(**{k: v for k, v in kwargs.items() if k in func.__code__.co_varnames})

async def aexec(code, client, message):
    exec(f"async def __aexec(client, message):\n" + "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexec"](client, message)

@ChatBot.on_message(filters.command("eval") & is_dev_filter())
async def executor(client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="No code provided!")
    cmd = message.text.split(None, 1)[1]
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = StringIO(), StringIO()
    exc = None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout, stderr = sys.stdout.getvalue(), sys.stderr.getvalue()
    sys.stdout, sys.stderr = old_stdout, old_stderr
    result = exc or stderr or stdout or "Success"
    await edit_or_reply(message, text=f"**Result:**\n{result}")
