"""
🚀 Self-Development Super Bot
27 ta funksiya — bitta botda!
"""
import logging
from datetime import time as dtime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from config import BOT_TOKEN, PROXY_URL
from database import init_db, ensure_user, get_full_stats, get_book_stats, get_daily_tasks, seed_default_daily_tasks
from data import get_daily_quote

from handlers import (
    daily_plan,
    habit_tracker,
    workout,
    language,
    book_tracker,
    videos,
    goals,
    stats,
    brain,
    focus_timer,
    knowledge_vault,
    reminders,
    motivation,
    mood_tracker,
    anti_procrastination,
    evening_review,
    morning_startup,
    nozero,
    score_system,
    quick_log,
    weekly_report,
    recommendations,
    mini_course,
    emergency_reset,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ========== /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    text = (
        f"🚀 <b>Xush kelibsiz, {user.first_name}!</b>\n\n"
        "Bu — <b>Self-Development Super Bot</b> 🧠\n"
        "Har kuni o'zingizni rivojlantiring!\n\n"
        "📱 <b>Asosiy funksiyalar:</b>\n\n"
        "📋 /plan — Kunlik reja\n"
        "🔥 /habits — Odatlar tracker\n"
        "💪 /workout — Trenirovka\n"
        "🌍 /language — Til o'rganish\n"
        "📚 /book — Kitob o'qish\n"
        "🎥 /videos — Foydali videolar\n"
        "🎯 /goals — Maqsadlar & Challengelar\n"
        "🎯 /focus — Focus timer (Pomodoro)\n"
        "🧠 /brain — Brain training\n"
        "📂 /vault — Knowledge vault\n"
        "⏰ /reminders — Eslatmalar\n"
        "💡 /motivation — Motivatsion fikr\n\n"
        "🆕 <b>Qo'shimcha funksiyalar:</b>\n\n"
        "😊 /mood — Kayfiyat tracker\n"
        "🛡 /antiprocrastination — Anti-prokrastinatsiya\n"
        "🌙 /evening — Kechki tahlil\n"
        "☀️ /morning — Ertalabki start\n"
        "📅 /nozero — No Zero Day\n"
        "⭐ /score — Ball tizimi\n"
        "⚡ /quicklog — Tez yozuv\n"
        "📊 /weekly — Haftalik hisobot\n"
        "💡 /recommend — Shaxsiy tavsiyalar\n"
        "📘 /course — Mini kurslar\n"
        "🚨 /emergency — Favqulodda reset\n\n"
        "📊 /stats — 30 kunlik | /stats90 — 90 kunlik\n"
        "🤖 /advice — AI maslahat\n\n"
        "Yoki quyidagi tugmalardan foydalaning 👇"
    )

    keyboard = [
        [
            InlineKeyboardButton("📋 Kunlik reja", callback_data="menu_plan"),
            InlineKeyboardButton("🔥 Odatlar", callback_data="menu_habits"),
        ],
        [
            InlineKeyboardButton("💪 Trenirovka", callback_data="menu_workout"),
            InlineKeyboardButton("🌍 Til o'rganish", callback_data="menu_language"),
        ],
        [
            InlineKeyboardButton("📚 Kitob o'qish", callback_data="menu_book"),
            InlineKeyboardButton("🎥 Videolar", callback_data="menu_videos"),
        ],
        [
            InlineKeyboardButton("🎯 Maqsadlar", callback_data="menu_goals"),
            InlineKeyboardButton("🎯 Focus Timer", callback_data="menu_focus"),
        ],
        [
            InlineKeyboardButton("🧠 Brain Training", callback_data="menu_brain"),
            InlineKeyboardButton("📊 Progress", callback_data="menu_stats"),
        ],
        [
            InlineKeyboardButton("📂 Vault", callback_data="menu_vault"),
            InlineKeyboardButton("⏰ Eslatmalar", callback_data="menu_reminders"),
        ],
        [
            InlineKeyboardButton("💡 Motivatsiya", callback_data="menu_motivation"),
            InlineKeyboardButton("🤖 AI Maslahat", callback_data="menu_advice"),
        ],
        [
            InlineKeyboardButton("😊 Kayfiyat", callback_data="menu_mood"),
            InlineKeyboardButton("🛡 Anti-prokr.", callback_data="menu_antiprocrastination"),
        ],
        [
            InlineKeyboardButton("🌙 Kechki tahlil", callback_data="menu_evening"),
            InlineKeyboardButton("☀️ Ertalab", callback_data="menu_morning"),
        ],
        [
            InlineKeyboardButton("📅 No Zero Day", callback_data="menu_nozero"),
            InlineKeyboardButton("⭐ Ball", callback_data="menu_score"),
        ],
        [
            InlineKeyboardButton("⚡ Tez yozuv", callback_data="menu_quicklog"),
            InlineKeyboardButton("📊 Haftalik", callback_data="menu_weekly"),
        ],
        [
            InlineKeyboardButton("💡 Tavsiyalar", callback_data="menu_recommend"),
            InlineKeyboardButton("📘 Kurslar", callback_data="menu_course"),
        ],
        [
            InlineKeyboardButton("🚨 Emergency Reset", callback_data="menu_emergency"),
        ],
    ]
    await update.message.reply_text(
        text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ========== Menu callbacks ==========
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    action = query.data.replace("menu_", "")
    await query.answer()

    handlers_map = {
        "plan": daily_plan.daily_plan_cmd,
        "habits": habit_tracker.habits_cmd,
        "workout": workout.workout_cmd,
        "language": language.language_cmd,
        "book": book_tracker.book_cmd,
        "videos": videos.videos_cmd,
        "goals": goals.goals_cmd,
        "focus": focus_timer.focus_cmd,
        "brain": brain.brain_cmd,
        "stats": stats.stats_cmd,
        "vault": knowledge_vault.vault_cmd,
        "reminders": reminders.reminder_cmd,
        "motivation": motivation.motivation_cmd,
        "advice": ai_advice,
        "mood": mood_tracker.mood_cmd,
        "antiprocrastination": anti_procrastination.antiprocrastination_cmd,
        "evening": evening_review.evening_cmd,
        "morning": morning_startup.morning_cmd,
        "nozero": nozero.nozero_cmd,
        "score": score_system.score_cmd,
        "quicklog": quick_log.quicklog_cmd,
        "weekly": weekly_report.weekly_cmd,
        "recommend": recommendations.recommend_cmd,
        "course": mini_course.course_cmd,
        "emergency": emergency_reset.emergency_cmd,
    }

    handler_fn = handlers_map.get(action)
    if handler_fn:
        await handler_fn(update, context)


# ========== /help ==========
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ <b>Yordam — Barcha buyruqlar</b>\n\n"
        "📋 /plan — Kunlik vazifalar\n"
        "🔥 /habits — Odat nazorati\n"
        "💪 /workout — Uy mashqlari\n"
        "🌍 /language — Ingliz tili\n"
        "📚 /book — Kitob tracker\n"
        "🎥 /videos — Foydali videolar\n"
        "🎯 /goals — Maqsad & Challenge\n"
        "🎯 /focus — Pomodoro timer\n"
        "🧠 /brain — Miya mashqlari\n"
        "📊 /stats — 30 kunlik statistika\n"
        "📈 /stats90 — 90 kunlik statistika\n"
        "📂 /vault — Bilim ombori\n"
        "⏰ /reminders — Eslatmalar\n"
        "💡 /motivation — Motivatsion fikr\n"
        "🤖 /advice — AI maslahat\n"
        "😊 /mood — Kayfiyat tracker\n"
        "🛡 /antiprocrastination — Anti-prokrastinatsiya\n"
        "🌙 /evening — Kechki tahlil\n"
        "☀️ /morning — Ertalabki start\n"
        "📅 /nozero — No Zero Day\n"
        "⭐ /score — Ball tizimi\n"
        "⚡ /quicklog — Tez yozuv\n"
        "📊 /weekly — Haftalik hisobot\n"
        "💡 /recommend — Shaxsiy tavsiyalar\n"
        "📘 /course — Mini kurslar\n"
        "🚨 /emergency — Favqulodda reset\n"
        "❌ /cancel — Amalni bekor qilish\n\n"
        "🆓 Bot 24/7 bepul ishlaydi!"
    )
    await update.message.reply_text(text, parse_mode="HTML")


# ========== 🤖 AI Maslahat ==========
async def ai_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)
    seed_default_daily_tasks(user.id)

    s = get_full_stats(user.id, days=7)
    book = get_book_stats(user.id)
    tasks = get_daily_tasks(user.id)
    done_tasks = sum(1 for t in tasks if t["is_done"])
    total_tasks = len(tasks)

    advices = []

    if s["workouts"] < 3:
        advices.append("🏃 Bu hafta trenirovka kam bo'ldi. Kamida 4-5 kun sport qilishni tavsiya qilaman!")
    else:
        advices.append("💪 Trenirovka bo'yicha zo'r ketayapsiz! Davom eting!")

    if book["week"] < 30:
        advices.append("📚 Bu hafta kitob o'qish juda kam. Har kuni 10 sahifa o'qing!")
    else:
        advices.append("📚 Kitob o'qish bo'yicha ajoyib! O'qishda davom eting!")

    if s["words"] < 15:
        advices.append("🌍 Ingliz tili so'zlari kam. Har kuni 5 ta yangi so'z o'rganing!")
    else:
        advices.append("🌍 So'z o'rganish yaxshi ketayapti!")

    if done_tasks < total_tasks and total_tasks > 0:
        advices.append(f"📋 Bugun {total_tasks - done_tasks} ta vazifa bajarilmagan. Hozir bajaring!")

    if s["videos"] == 0:
        advices.append("🎥 Bu hafta foydali video ko'rmadingiz. 1 ta video ko'ring!")

    quote = get_daily_quote()
    advices.append(f"\n💡 {quote}")

    text = "🤖 <b>AI Maslahat</b>\n\n" + "\n\n".join(advices)

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML")


# ========== SET BOT COMMANDS ==========
async def post_init(app: Application):
    commands = [
        BotCommand("start", "🚀 Boshlash"),
        BotCommand("plan", "📋 Kunlik reja"),
        BotCommand("habits", "🔥 Odatlar"),
        BotCommand("workout", "💪 Trenirovka"),
        BotCommand("language", "🌍 Til o'rganish"),
        BotCommand("book", "📚 Kitob o'qish"),
        BotCommand("videos", "🎥 Foydali videolar"),
        BotCommand("goals", "🎯 Maqsadlar"),
        BotCommand("focus", "🎯 Focus timer"),
        BotCommand("brain", "🧠 Brain training"),
        BotCommand("stats", "📊 30 kun statistika"),
        BotCommand("stats90", "📈 90 kun statistika"),
        BotCommand("vault", "📂 Knowledge vault"),
        BotCommand("reminders", "⏰ Eslatmalar"),
        BotCommand("motivation", "💡 Motivatsiya"),
        BotCommand("advice", "🤖 AI maslahat"),
        BotCommand("mood", "😊 Kayfiyat tracker"),
        BotCommand("antiprocrastination", "🛡 Anti-prokrastinatsiya"),
        BotCommand("evening", "🌙 Kechki tahlil"),
        BotCommand("morning", "☀️ Ertalabki start"),
        BotCommand("nozero", "📅 No Zero Day"),
        BotCommand("score", "⭐ Ball tizimi"),
        BotCommand("quicklog", "⚡ Tez yozuv"),
        BotCommand("weekly", "📊 Haftalik hisobot"),
        BotCommand("recommend", "💡 Tavsiyalar"),
        BotCommand("course", "📘 Mini kurslar"),
        BotCommand("emergency", "🚨 Favqulodda reset"),
        BotCommand("help", "ℹ️ Yordam"),
    ]
    await app.bot.set_my_commands(commands)


# ========== MAIN ==========
def main():
    init_db()

    builder = Application.builder().token(BOT_TOKEN).post_init(post_init)
    if PROXY_URL:
        from telegram.request import HTTPXRequest
        request = HTTPXRequest(proxy=PROXY_URL, connect_timeout=20, read_timeout=30)
        get_request = HTTPXRequest(proxy=PROXY_URL, connect_timeout=20, read_timeout=30)
        builder = builder.request(request).get_updates_request(get_request)
    app = builder.build()

    # Core commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("advice", ai_advice))

    # Menu callback
    app.add_handler(CallbackQueryHandler(menu_callback, pattern=r"^menu_"))

    # Register all 24 modules
    daily_plan.register(app)
    habit_tracker.register(app)
    workout.register(app)
    language.register(app)
    book_tracker.register(app)
    videos.register(app)
    goals.register(app)
    stats.register(app)
    brain.register(app)
    focus_timer.register(app)
    knowledge_vault.register(app)
    reminders.register(app)
    motivation.register(app)
    mood_tracker.register(app)
    anti_procrastination.register(app)
    evening_review.register(app)
    morning_startup.register(app)
    nozero.register(app)
    score_system.register(app)
    quick_log.register(app)
    weekly_report.register(app)
    recommendations.register(app)
    mini_course.register(app)
    emergency_reset.register(app)

    # Job queue — avtomatik vazifalar
    tz = pytz.timezone("Asia/Tashkent")
    job_queue = app.job_queue
    if job_queue:
        # Eslatma tekshiruv (har 60 soniyada)
        job_queue.run_repeating(
            reminders.check_reminders,
            interval=60,
            first=10,
            name="reminder_checker",
        )
        # Ertalabki xabar — 06:00
        job_queue.run_daily(
            morning_startup.send_morning_message,
            time=dtime(6, 0, tzinfo=tz),
            name="morning_message",
        )
        # No Zero Day eslatma — 21:00
        job_queue.run_daily(
            nozero.send_nozero_reminder,
            time=dtime(21, 0, tzinfo=tz),
            name="nozero_reminder",
        )
        # Kunlik jarima tekshiruvi — 23:50
        job_queue.run_daily(
            score_system.check_daily_penalties,
            time=dtime(23, 50, tzinfo=tz),
            name="daily_penalties",
        )
        # Haftalik hisobot — Yakshanba 20:00
        job_queue.run_daily(
            weekly_report.send_weekly_report,
            time=dtime(20, 0, tzinfo=tz),
            days=(6,),
            name="weekly_report",
        )

    logger.info("Bot ishga tushdi! 🚀 27 ta funksiya tayyor!")

    from config import MODE, PORT, RENDER_URL
    if MODE == "webhook" and RENDER_URL:
        webhook_url = f"{RENDER_URL}/webhook"
        logger.info(f"Webhook rejim: {webhook_url}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path="/webhook",
            webhook_url=webhook_url,
            allowed_updates=Update.ALL_TYPES,
        )
    else:
        app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
