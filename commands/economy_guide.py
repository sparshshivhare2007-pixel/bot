from telegram import Update
from telegram.ext import CallbackContext

async def economy_guide(update: Update, context: CallbackContext):
    """Sends the Baka Economy System Guide to the user."""
    
    guide_text = (
        "💰 *Akeno Economy System Guide*\n\n"
        
        "💬 *How it works:*\n"
        "Manage your virtual money and items in the group! Use commands below to earn, gift, buy, or interact with others.\n\n"
        
        "🔨 *Economy Commands:*\n"
        "🔹 `/close` — Close economy commands working in the group\n"
        "🔹 `/open` — Open economy commands working in the group\n"
        "🔹 `/bal` — Check your/friend's balance\n"
        "🔹 `/toprich` — See top 10 richest users\n"
        "🔹 `/topkill` — See top 10 killers\n"
        "🔹 `/give` (Reply) `amount` — Gift money to someone\n"
        "🔹 `/rob` (Reply) `amount` (1-100000) — Rob someone\n"
        "🔹 `/kill` (Reply) — Kill someone\n"
        "🔹 `/revive` (Reply or without reply) — Revive you or your friend\n"
        "🔹 `/protect 1d|2d` — Buy protection\n"
        "🔹 `/transfer amount` — Owner only: Add/remove money\n\n"
        
        "🎁 *Item & Gifting*\n"
        "• Earn money by killing others\n"
        "• Gift money with 10% fee\n"
        "• Buy protection to avoid robbery\n"
        "• Top rankings for richest and killers"
    )

    await update.message.reply_text(
        guide_text,
        parse_mode="Markdown"
    )
