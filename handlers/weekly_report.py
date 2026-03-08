"""📊 Haftalik hisobot handler"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import (
    ensure_user, get_weekly_stats, get_book_stats, get_focus_stats,
    get_non_zero_streak, get_total_score, get_mood_averages, get_all_users,
)
from handlers.score_system import get_level


async def weekly_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)
    text = _build_weekly_report(user.id)
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML")


def _build_weekly_report(user_id):
    s = get_weekly_stats(user_id)
    book = get_book_stats(user_id)
    focus = get_focus_stats(user_id, 7)
    streak = get_non_zero_streak(user_id)
    total_score = get_total_score(user_id)
    level_name, _ = get_level(total_score)
    mood = get_mood_averages(user_id, 7)

    areas = {
        "💪 Sport": s["workouts"],
        "📚 Kitob": book["week"],
        "🌍 Til": s["words"],
        "🎯 Focus": focus["total_minutes"],
        "🔥 Odat": s["habit_days"],
    }
    strongest = max(areas, key=areas.get) if areas else "—"
    weakest = min(areas, key=areas.get) if areas else "—"

    lines = [
        "📊 <b>HAFTALIK HISOBOT</b>\n",
        f"🏅 Daraja: {level_name} | ⭐ {total_score} ball",
        f"🔥 Streak: {streak} kun\n",
        "<b>📈 Haftalik natijalar:</b>",
        f"  💪 Trenirovkalar: {s['workouts']} marta",
        f"  📚 Kitob: {book['week']} sahifa",
        f"  🌍 So'zlar: {s['words']} ta",
        f"  🎥 Videolar: {s['videos']} ta",
        f"  🎯 Focus: {focus['total_minutes']} daqiqa",
        f"  🔥 Odat kunlari: {s['habit_days']}",
    ]

    if mood["count"] > 0:
        lines.append(
            f"\n😊 Kayfiyat: {mood['avg_mood']} | "
            f"⚡ Energiya: {mood['avg_energy']} | "
            f"🧘 Stress: {mood['avg_stress']}"
        )

    lines.append(f"\n💪 <b>Eng kuchli:</b> {strongest}")
    lines.append(f"📉 <b>Eng zaif:</b> {weakest} — bunga ko'proq e'tibor bering!")
    lines.append("\n🚀 Kelasi hafta yana zo'r bo'lsin!")

    return "\n".join(lines)


async def send_weekly_report(context: ContextTypes.DEFAULT_TYPE):
    """Job queue orqali har yakshanba avtomatik hisobot"""
    users = get_all_users()
    for uid in users:
        try:
            text = _build_weekly_report(uid)
            await context.bot.send_message(uid, text, parse_mode="HTML")
        except Exception:
            pass


def register(app):
    app.add_handler(CommandHandler("weekly", weekly_cmd))
