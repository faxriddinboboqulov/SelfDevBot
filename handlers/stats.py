"""📊 Statistika handler"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import ensure_user, get_full_stats, get_book_stats, get_focus_stats, get_total_score, get_non_zero_streak


def _make_bar(value, max_val):
    if max_val <= 0:
        return "⬜" * 10
    filled = min(10, int(value / max_val * 10))
    return "🟩" * filled + "⬜" * (10 - filled)


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
    score = get_total_score(user_id)
    streak = get_non_zero_streak(user_id)

    level = score // 100
    level_names = ["Yangi boshlovchi", "Faol", "Izchil", "Kuchli", "Professional", "Ekspert", "Legenda", "GOAT"]
    rank = level_names[min(level, len(level_names) - 1)]
    next_lvl = (level + 1) * 100
    lvl_progress = score % 100

    text = (
        f"📊 <b>{days} kunlik statistika</b>\n\n"
        f"🏆 <b>Ball:</b> {score} ⭐ | <b>Daraja:</b> {rank}\n"
        f"📈 Keyingi daraja: {_make_bar(lvl_progress, 100)} {lvl_progress}/100\n"
        f"🔥 <b>Streak:</b> {streak} kun\n\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"💪 Trenirovkalar: <b>{s['workouts']}</b> marta\n"
        f"📚 Kitob: <b>{s['pages']}</b> sahifa\n"
        f"🌍 So'zlar: <b>{s['words']}</b> ta\n"
        f"🎥 Videolar: <b>{s['videos']}</b> ta\n"
        f"🎯 Focus: <b>{focus['total_minutes']}</b> daqiqa ({focus['sessions']} sessiya)\n"
        f"🔥 Odat kunlari: <b>{s['habit_days']}</b> kun\n\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"📖 <b>Kitob tafsiloti:</b>\n"
        f"  Hafta: {book['week']}p | Oy: {book['month']}p | Jami: {book['total']}p"
    )

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML")


def register(app):
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("stats90", stats90_cmd))
