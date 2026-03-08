"""📊 Statistika handler"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import ensure_user, get_full_stats, get_book_stats, get_focus_stats


async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)
    await _show_stats(update, user.id, 30)


async def stats90_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)
    await _show_stats(update, user.id, 90)


async def _show_stats(update, user_id, days):
    s = get_full_stats(user_id, days)
    book = get_book_stats(user_id)
    focus = get_focus_stats(user_id, days)

    text = (
        f"📊 <b>{days} kunlik statistika</b>\n\n"
        f"💪 Trenirovkalar: {s['workouts']} marta\n"
        f"📚 Kitob: {s['pages']} sahifa\n"
        f"🌍 So'zlar: {s['words']} ta\n"
        f"🎥 Videolar: {s['videos']} ta\n"
        f"🎯 Focus: {focus['total_minutes']} daqiqa ({focus['sessions']} sessiya)\n"
        f"🔥 Odat kunlari: {s['habit_days']} kun\n\n"
        f"📖 Kitob (hafta/oy/jami): {book['week']}/{book['month']}/{book['total']} sahifa"
    )

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML")


def register(app):
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("stats90", stats90_cmd))
