"""⏰ Eslatmalar handler"""
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters,
)
from database import ensure_user, add_reminder, get_user_reminders, get_pending_reminders, mark_reminder_sent

SETTING_TIME = 0
SETTING_TEXT = 1


async def reminder_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    reminders = get_user_reminders(user.id)
    lines = ["⏰ <b>Eslatmalar</b>\n"]
    if reminders:
        for r in reminders:
            status = "✅" if r["is_sent"] else "⏳"
            lines.append(f"{status} {r['remind_time']} — {r['text']}")
    else:
        lines.append("📭 Bugungi eslatmalar yo'q.")

    buttons = [
        [InlineKeyboardButton("➕ Yangi eslatma", callback_data="rem_add")],
    ]
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text("\n".join(lines), parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def rem_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("⏰ Eslatma vaqtini kiriting (HH:MM formatda, masalan: 14:30):")
    return SETTING_TIME


async def rem_set_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not re.match(r"^\d{1,2}:\d{2}$", text):
        await update.message.reply_text("❌ Noto'g'ri format. HH:MM formatda yozing (masalan: 14:30):")
        return SETTING_TIME

    parts = text.split(":")
    h, m = int(parts[0]), int(parts[1])
    if h < 0 or h > 23 or m < 0 or m > 59:
        await update.message.reply_text("❌ Noto'g'ri vaqt. 00:00 - 23:59 orasida bo'lishi kerak.")
        return SETTING_TIME

    context.user_data["rem_time"] = f"{h:02d}:{m:02d}"
    await update.message.reply_text("📝 Eslatma matnini yozing:")
    return SETTING_TEXT


async def rem_set_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if len(text) > 500:
        await update.message.reply_text("❌ Matn juda uzun (max 500 belgi).")
        return SETTING_TEXT
    remind_time = context.user_data.get("rem_time", "12:00")
    add_reminder(update.effective_user.id, text, remind_time)
    await update.message.reply_text(
        f"✅ Eslatma saqlandi!\n⏰ {remind_time} da: {text}"
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.")
    return ConversationHandler.END


async def check_reminders(context: ContextTypes.DEFAULT_TYPE):
    """Job queue orqali har daqiqada tekshirish"""
    pending = get_pending_reminders()
    for r in pending:
        try:
            await context.bot.send_message(
                r["user_id"],
                f"🔔 <b>Eslatma!</b>\n\n{r['text']}",
                parse_mode="HTML",
            )
            mark_reminder_sent(r["id"])
        except Exception:
            pass


def register(app):
    app.add_handler(CommandHandler("reminders", reminder_cmd))
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(rem_add_start, pattern=r"^rem_add$")],
        states={
            SETTING_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, rem_set_time)],
            SETTING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, rem_set_text)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False,
    )
    app.add_handler(conv)
