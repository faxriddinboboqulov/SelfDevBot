"""📋 Kunlik reja handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import ensure_user, seed_default_daily_tasks, get_daily_tasks, toggle_task
from data import get_celebration


async def daily_plan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)
    seed_default_daily_tasks(user.id)
    await _show_tasks(update, user.id)


async def _show_tasks(update, user_id):
    tasks = get_daily_tasks(user_id)
    if not tasks:
        text = "📋 Bugun uchun vazifalar yo'q."
        msg = update.callback_query.message if update.callback_query else update.message
        await msg.reply_text(text)
        return

    lines = ["📋 <b>Bugungi vazifalar:</b>\n"]
    buttons = []
    done_count = 0
    for t in tasks:
        status = "✅" if t["is_done"] else "⬜"
        lines.append(f"{status} {t['title']}")
        if t["is_done"]:
            done_count += 1
        buttons.append(
            [InlineKeyboardButton(
                f"{'✅' if t['is_done'] else '⬜'} {t['title']}",
                callback_data=f"task_toggle_{t['id']}",
            )]
        )

    pct = int(done_count / len(tasks) * 100)
    bar_filled = pct // 10
    bar = "🟩" * bar_filled + "⬜" * (10 - bar_filled)
    lines.append(f"\n{bar} {pct}% ({done_count}/{len(tasks)})")

    if pct == 100:
        lines.append(f"\n🎉🎉🎉 BARCHA VAZIFALAR BAJARILDI! {get_celebration()}")
    elif pct >= 75:
        lines.append("\n🔥 Deyarli tayyor! Oxirgi zarba!")
    elif pct >= 50:
        lines.append("\n💪 Yarmidan ko'p — davom eting!")
    elif done_count > 0:
        lines.append("\n⚡ Yaxshi boshlangach, davom eting!")

    text = "\n".join(lines)
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def task_toggle_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    task_id = int(q.data.split("_")[-1])
    toggle_task(task_id, q.from_user.id)
    await _show_tasks(update, q.from_user.id)


def register(app):
    app.add_handler(CommandHandler("plan", daily_plan_cmd))
    app.add_handler(CallbackQueryHandler(task_toggle_cb, pattern=r"^task_toggle_"))
