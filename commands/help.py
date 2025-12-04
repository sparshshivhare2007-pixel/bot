from main import app
from pyrogram import filters
from pyrogram.types import Message

@app.on_message(filters.command('help') & filters.private)
async def help_cmd(client, message: Message):
    text = '''Available commands (private):
/balance /daily /work /beg /deposit /withdraw /transfer /shop /buy /sell /inventory /profile /leaderboard /coinflip /slots /dice /gamble /lottery /marry /divorce /gift /stats /help
Group commands: /rob (reply), /leaderboard_group
Admin: /addbal /resetuser
'''
    await message.reply(text)
