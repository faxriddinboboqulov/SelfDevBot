"""💡 Motivatsiya handler"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import ensure_user, get_non_zero_streak
from data import get_daily_quote, get_fun_fact


async def motivation_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)
    quote = get_daily_quote()
    fact = get_fun_fact()
    streak = get_non_zero_streak(user.id)

    streak_msg = ""
    if streak >= 7:
        streak_msg = f"\n🔥 {streak} kunlik streak! Ajoyib davom etyapsiz!"
    elif streak >= 1:
        streak_msg = f"\n🔥 {streak} kunlik streak — davom eting!"
    else:
        streak_msg = "\n⚡ Bugun streakni boshlang!"

    text = (
        f"💡 <b>Bugungi motivatsiya:</b>\n\n"
        f"{quote}\n"
        f"{streak_msg}\n\n"
        f"🧠 <b>Qiziqarli fakt:</b>\n{fact}"
    )
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML")


def register(app):
    app.add_handler(CommandHandler("motivation", motivation_cmd))
