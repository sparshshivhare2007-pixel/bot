# Pyrogram Economy Bot (Ready-to-run)

**What you got:** a small but complete Pyrogram-based economy bot with:
- MongoDB (motor) for persistence
- Commands: /start, /balance, /daily, /work, /beg, /rob, /deposit, /withdraw, /leaderboard
- Simple folder structure and example config
- Ready to run locally (fill config values)

## Quick setup
1. Install Python 3.10+.
2. Create a virtualenv and activate it.
3. `pip install -r requirements.txt`
4. Edit `config.py` and put your `API_ID`, `API_HASH`, `BOT_TOKEN` and `MONGO_DB_URL`.
5. Run: `python main.py`

## Notes
- Use a MongoDB URI (e.g., MongoDB Atlas). If you want a local fallback (JSON), modify `database/db.py`.
- This project is educational. Don't use it to spam or abuse Telegram.
