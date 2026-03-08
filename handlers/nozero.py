"""📅 No Zero Day handler"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import ensure_user, is_zero_day, get_non_zero_streak, get_all_users


async def nozero_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    zero = is_zero_day(user.id)
    streak = get_non_zero_streak(user.id)

    if zero:
        text = (
            "📅 <b>No Zero Day</b>\n\n"
            "🚨 <b>Bugun hali hech narsa qilmadingiz!</b>\n\n"
            f"🔥 Joriy streak: {streak} kun\n\n"
            "Hozir bironta foydali ish qiling:\n"
            "• /workout — Trenirovka\n"
            "• /book — Kitob o'qish\n"
            "• /language — So'z o'rganish\n"
            "• /focus — Focus sessiya\n"
            "• /emergency — Favqulodda mini-reja"
        )
    else:
        text = (
            "📅 <b>No Zero Day</b>\n\n"
            "✅ <b>Bugun zero day EMAS!</b> Yaxshi ish!\n\n"
            f"🔥 Joriy streak: {streak} kun\n\n"
            "Davom eting! 💪"
        )

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML")


async def send_nozero_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Job queue orqali kechqurun eslatma"""
    users = get_all_users()
    for uid in users:
        try:
            if is_zero_day(uid):
                await context.bot.send_message(
                    uid,
                    "🚨 <b>No Zero Day eslatma!</b>\n\n"
                    "Bugun hali hech narsa qilmadingiz!\n"
                    "Kamida 1 ta ish qiling:\n"
                    "• /emergency — Tez mini-reja\n"
                    "• /quicklog — Tez yozuv",
                    parse_mode="HTML",
                )
        except Exception:
            pass


def register(app):
    app.add_handler(CommandHandler("nozero", nozero_cmd))
