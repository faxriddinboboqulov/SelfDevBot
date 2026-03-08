"""🚨 Favqulodda reset handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import (
    ensure_user, log_workout, log_book_pages, add_focus_session, add_word, add_score,
)

EMERGENCY_PLAN = [
    ("🏋️ 1 ta engil mashq", "emg_workout"),
    ("📖 5 sahifa o'qish", "emg_book"),
    ("🎯 5 daqiqa fokus", "emg_focus"),
    ("🌍 3 ta so'z o'rganish", "emg_words"),
]


async def emergency_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    buttons = [
        [InlineKeyboardButton(f"✅ {label}", callback_data=cb)]
        for label, cb in EMERGENCY_PLAN
    ]
    buttons.append(
        [InlineKeyboardButton("⚡ HAMMASINI bajarildi deb belgilash", callback_data="emg_all")]
    )

    text = (
        "🚨 <b>Favqulodda qayta boshlash!</b>\n\n"
        "Ruhingiz tushganmi? Streak uzilganmi?\n"
        "Hech gap yo'q — shu 4 ta oddiy ishni bajaring va qaytadan boshlang:\n\n"
        "🏋️ 1 ta engil mashq\n"
        "📖 5 sahifa o'qish\n"
        "🎯 5 daqiqa fokus\n"
        "🌍 3 ta so'z o'rganish\n\n"
        "Har birini bajargach ✅ tugmasini bosing!"
    )

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML")


async def emergency_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    data = q.data

    if data == "emg_workout":
        log_workout(uid, "Engil mashq", "Beginner")
        add_score(uid, "workout", 5, "Emergency mashq")
        await q.message.reply_text("✅ 1 ta engil mashq bajarildi! +5 ⭐")

    elif data == "emg_book":
        log_book_pages(uid, 5)
        add_score(uid, "book", 3, "Emergency 5 sahifa")
        await q.message.reply_text("✅ 5 sahifa o'qish bajarildi! +3 ⭐")

    elif data == "emg_focus":
        add_focus_session(uid, 5)
        add_score(uid, "focus", 3, "Emergency 5 min focus")
        await q.message.reply_text("✅ 5 daqiqa fokus bajarildi! +3 ⭐")

    elif data == "emg_words":
        for w in ["hello - salom", "book - kitob", "run - yugurmoq"]:
            add_word(uid, w)
        add_score(uid, "language", 3, "Emergency 3 so'z")
        await q.message.reply_text("✅ 3 ta so'z o'rganish bajarildi! +3 ⭐")

    elif data == "emg_all":
        log_workout(uid, "Engil mashq", "Beginner")
        log_book_pages(uid, 5)
        add_focus_session(uid, 5)
        for w in ["hello - salom", "book - kitob", "run - yugurmoq"]:
            add_word(uid, w)
        add_score(uid, "workout", 5, "Emergency mashq")
        add_score(uid, "book", 3, "Emergency 5 sahifa")
        add_score(uid, "focus", 3, "Emergency 5 min focus")
        add_score(uid, "language", 3, "Emergency 3 so'z")
        await q.message.reply_text(
            "⚡ <b>Barcha mini-topshiriqlar bajarildi!</b>\n"
            "Siz qaytib kelyapsiz! 💪 +14 ⭐",
            parse_mode="HTML",
        )


def register(app):
    app.add_handler(CommandHandler("emergency", emergency_cmd))
    app.add_handler(CallbackQueryHandler(emergency_callback, pattern=r"^emg_"))
