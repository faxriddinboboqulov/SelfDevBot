"""☀️ Ertalabki start handler"""
import random
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import ensure_user, get_goals, get_non_zero_streak, get_all_users
from data import get_daily_quote, get_fun_fact


async def morning_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)
    text = _build_morning_text(user.id, user.first_name)
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML")


def _build_morning_text(user_id, name):
    quote = get_daily_quote()
    goals = get_goals(user_id)
    streak = get_non_zero_streak(user_id)
    fact = get_fun_fact()

    # Dynamic streak message
    if streak >= 30:
        streak_msg = f"🔥🔥🔥 {streak} kunlik mega streak! LEGENDA!"
    elif streak >= 14:
        streak_msg = f"🔥🔥 {streak} kunlik streak! To'xtab bo'lmaydi!"
    elif streak >= 7:
        streak_msg = f"🔥 {streak} kunlik streak! Ajoyib ritm!"
    elif streak >= 1:
        streak_msg = f"🔥 {streak} kunlik streak — bugun ham davom!"
    else:
        streak_msg = "⚡ Yangi kun — yangi streak boshlanishi!"

    morning_vibes = [
        "🌞 Yangi kun — yangi imkoniyat!",
        "☕ Qahva + maqsad = ajoyib kun!",
        "🚀 Bugun kechagidan yaxshiroq bo'lasiz!",
        "🏆 G'oliblar ertalab boshlaydi!",
        "💪 Har bir tong — yangi boshlash!",
    ]

    lines = [
        f"☀️ <b>Xayrli tong, {name}!</b>\n",
        f"{random.choice(morning_vibes)}\n",
        f"💡 <i>{quote}</i>\n",
        f"{streak_msg}\n",
    ]

    if goals:
        lines.append("🎯 <b>Faol maqsadlar:</b>")
        for g in goals[:3]:
            pct = int(g["progress"] / g["target"] * 100) if g["target"] > 0 else 0
            bar_filled = pct // 20
            bar = "█" * bar_filled + "░" * (5 - bar_filled)
            lines.append(f"  • {g['title']} [{bar}] {pct}%")

    lines.append(f"\n🧠 <b>Bugungi fakt:</b> {fact}")
    lines.append("\n💪 <b>Bugun ham o'sish kuni! Boshlang!</b>")
    return "\n".join(lines)


async def send_morning_message(context: ContextTypes.DEFAULT_TYPE):
    """Job queue orqali har kuni ertalab avtomatik xabar"""
    users = get_all_users()
    for uid in users:
        try:
            text = _build_morning_text(uid, "do'stim")
            await context.bot.send_message(uid, text, parse_mode="HTML")
        except Exception:
            pass


def register(app):
    app.add_handler(CommandHandler("morning", morning_cmd))
