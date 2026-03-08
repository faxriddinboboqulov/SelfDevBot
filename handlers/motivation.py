"""💡 Motivatsiya handler"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import ensure_user
from data import get_daily_quote


async def motivation_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)
    quote = get_daily_quote()
    text = f"💡 <b>Bugungi motivatsiya:</b>\n\n{quote}"
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML")


def register(app):
    app.add_handler(CommandHandler("motivation", motivation_cmd))
