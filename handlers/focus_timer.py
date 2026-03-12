"""🎯 Focus Timer (Pomodoro) handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import ensure_user, add_focus_session, get_focus_stats, add_score, check_and_unlock_achievements
from data import get_focus_cheer, ACHIEVEMENTS


async def focus_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    stats = get_focus_stats(user.id, 7)
    text = (
        "🎯 <b>Focus Timer (Pomodoro)</b>\n\n"
        f"📊 Bu hafta: {stats['total_minutes']} daqiqa ({stats['sessions']} sessiya)\n\n"
        "Vaqtni tanlang:"
    )
    buttons = [
        [
            InlineKeyboardButton("⏱ 10 min", callback_data="focus_10"),
            InlineKeyboardButton("⏱ 25 min", callback_data="focus_25"),
        ],
        [
            InlineKeyboardButton("⏱ 45 min", callback_data="focus_45"),
            InlineKeyboardButton("⏱ 60 min", callback_data="focus_60"),
        ],
    ]
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def focus_start_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    minutes = int(q.data.replace("focus_", ""))
    user_id = q.from_user.id

    await q.message.reply_text(
        f"🎯 <b>{minutes} daqiqalik focus sessiya boshlandi!</b>\n\n"
        f"⏱ {minutes} daqiqadan keyin xabar olasiz.\n"
        "Diqqatingizni jamlab ishlang! 💪",
        parse_mode="HTML",
    )

    context.job_queue.run_once(
        _focus_done,
        when=minutes * 60,
        data={"user_id": user_id, "minutes": minutes},
        name=f"focus_{user_id}",
    )


async def _focus_done(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    user_id = data["user_id"]
    minutes = data["minutes"]
    add_focus_session(user_id, minutes)
    pts = minutes // 5
    add_score(user_id, "focus", pts, f"{minutes} min focus")
    cheer = get_focus_cheer()
    await context.bot.send_message(
        user_id,
        f"🔔🎉 <b>{minutes} daqiqalik focus sessiya tugadi!</b>\n\n"
        f"{cheer}\n\n"
        f"✅ +{pts} ⭐ ball qo'shildi!\n\n"
        "Dam oling 5 daqiqa, keyin yana boshlang! 💪",
        parse_mode="HTML",
    )

    # Check achievements
    new_badges = check_and_unlock_achievements(user_id)
    if new_badges:
        badge_lines = []
        for b in new_badges:
            a = ACHIEVEMENTS.get(b, {})
            badge_lines.append(f"{a.get('emoji','')} {a.get('title', b)}")
        await context.bot.send_message(
            user_id,
            "🏆 <b>YANGI YUTUQ OCHILDI!</b>\n\n" + "\n".join(badge_lines),
            parse_mode="HTML",
        )


def register(app):
    app.add_handler(CommandHandler("focus", focus_cmd))
    app.add_handler(CallbackQueryHandler(focus_start_cb, pattern=r"^focus_\d+$"))
