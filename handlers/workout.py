"""💪 Trenirovka handler"""
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import ensure_user, log_workout, add_score, get_workout_count, check_and_unlock_achievements
from data import WORKOUTS, get_workout_cheer, get_fun_fact, ACHIEVEMENTS


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
    uid = q.from_user.id
    level = q.data.replace("wodone_", "")
    log_workout(uid, f"{level} trenirovka", level)
    add_score(uid, "workout", 10, f"{level} trenirovka")
    cheer = get_workout_cheer()
    week_count = get_workout_count(uid, 7)
    fact = get_fun_fact()

    level_bonus = {"Beginner": "", "Intermediate": "\n🎖 Daraja bonusi: +2 ⭐", "Hard": "\n🏅 HARD daraja bonusi: +5 ⭐"}
    bonus_text = level_bonus.get(level, "")
    if level == "Intermediate":
        add_score(uid, "workout", 2, "Intermediate bonus")
    elif level == "Hard":
        add_score(uid, "workout", 5, "Hard bonus")

    text = (
        f"🎉🎉🎉\n\n"
        f"<b>{cheer}</b>\n\n"
        f"✅ <b>{level}</b> trenirovka bajarildi! +10 ⭐{bonus_text}\n"
        f"📊 Bu hafta: {week_count} ta trenirovka\n\n"
        f"💡 {fact}"
    )
    await q.message.reply_text(text, parse_mode="HTML")

    # Check achievements
    new_badges = check_and_unlock_achievements(uid)
    if new_badges:
        badge_lines = []
        for b in new_badges:
            a = ACHIEVEMENTS.get(b, {})
            badge_lines.append(f"{a.get('emoji','')} {a.get('title', b)}")
        await q.message.reply_text(
            "🏆 <b>YANGI YUTUQ OCHILDI!</b>\n\n" + "\n".join(badge_lines),
            parse_mode="HTML",
        )


def register(app):
    app.add_handler(CommandHandler("workout", workout_cmd))
    app.add_handler(CallbackQueryHandler(workout_level_cb, pattern=r"^wo_"))
    app.add_handler(CallbackQueryHandler(workout_done_cb, pattern=r"^wodone_"))
