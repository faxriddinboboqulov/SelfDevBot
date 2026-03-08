"""🔥 Odatlar tracker handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters,
)
from database import ensure_user, add_habit, get_habits, log_habit, get_habit_streak, is_habit_done_today

ADDING_HABIT = 0


async def habits_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)
    habits = get_habits(user.id)

    if not habits:
        text = (
            "🔥 <b>Odatlar tracker</b>\n\n"
            "Sizda hali odat yo'q.\n"
            "Yangi odat qo'shish uchun quyidagi tugmani bosing."
        )
    else:
        lines = ["🔥 <b>Odatlaringiz:</b>\n"]
        for h in habits:
            done = is_habit_done_today(h["id"], user.id)
            streak = get_habit_streak(h["id"], user.id)
            status = "✅" if done else "⬜"
            lines.append(f"{status} {h['name']} — 🔥 {streak} kun streak")
        text = "\n".join(lines)

    buttons = []
    for h in habits:
        done = is_habit_done_today(h["id"], user.id)
        if not done:
            buttons.append(
                [InlineKeyboardButton(f"✅ {h['name']}", callback_data=f"hlog_{h['id']}")]
            )
    buttons.append([InlineKeyboardButton("➕ Yangi odat qo'shish", callback_data="habit_add")])

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def habit_log_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    habit_id = int(q.data.split("_")[-1])
    result = log_habit(habit_id, q.from_user.id)
    if result:
        streak = get_habit_streak(habit_id, q.from_user.id)
        await q.message.reply_text(f"✅ Odat bajarildi! 🔥 Streak: {streak} kun")
    else:
        await q.message.reply_text("ℹ️ Bu odat bugun allaqachon bajarilgan.")


async def habit_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("📝 Yangi odat nomini yozing:")
    return ADDING_HABIT


async def habit_add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = update.message.text.strip()
    if len(name) > 100:
        await update.message.reply_text("❌ Odat nomi juda uzun (max 100 belgi)")
        return ADDING_HABIT
    add_habit(user.id, name)
    await update.message.reply_text(f"✅ <b>'{name}'</b> odati qo'shildi!", parse_mode="HTML")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.")
    return ConversationHandler.END


def register(app):
    app.add_handler(CommandHandler("habits", habits_cmd))
    app.add_handler(CallbackQueryHandler(habit_log_cb, pattern=r"^hlog_"))
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(habit_add_start, pattern=r"^habit_add$")],
        states={
            ADDING_HABIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, habit_add_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
