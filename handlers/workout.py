"""💪 Trenirovka handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import ensure_user, log_workout
from data import WORKOUTS


async def workout_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    text = (
        "💪 <b>Trenirovka</b>\n\n"
        "Darajangizni tanlang:"
    )
    buttons = [
        [InlineKeyboardButton(f"🟢 Beginner", callback_data="wo_Beginner")],
        [InlineKeyboardButton(f"🟡 Intermediate", callback_data="wo_Intermediate")],
        [InlineKeyboardButton(f"🔴 Hard", callback_data="wo_Hard")],
    ]
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def workout_level_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    level = q.data.replace("wo_", "")
    exercises = WORKOUTS.get(level, [])

    lines = [f"💪 <b>{level} trenirovka:</b>\n"]
    for ex in exercises:
        lines.append(f"{ex['emoji']} <b>{ex['name']}</b> — {ex['reps']}")

    lines.append("\nBarcha mashqlarni bajardingizmi?")

    buttons = [[InlineKeyboardButton("✅ Bajardim!", callback_data=f"wodone_{level}")]]
    await q.message.reply_text(
        "\n".join(lines), parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons)
    )


async def workout_done_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    level = q.data.replace("wodone_", "")
    log_workout(q.from_user.id, f"{level} trenirovka", level)
    await q.message.reply_text(f"🎉 <b>{level}</b> trenirovka bajarildi! +10 ⭐", parse_mode="HTML")


def register(app):
    app.add_handler(CommandHandler("workout", workout_cmd))
    app.add_handler(CallbackQueryHandler(workout_level_cb, pattern=r"^wo_"))
    app.add_handler(CallbackQueryHandler(workout_done_cb, pattern=r"^wodone_"))
