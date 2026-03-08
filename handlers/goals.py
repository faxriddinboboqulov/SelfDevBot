"""🎯 Maqsadlar & Challengelar handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters,
)
from database import (
    ensure_user, add_goal, get_goals, update_goal_progress,
    add_challenge, get_active_challenges, log_challenge_day, get_challenge_progress,
)
from data import CHALLENGE_TEMPLATES

ADDING_GOAL = 0
GOAL_PROGRESS = 1


async def goals_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    goals = get_goals(user.id)
    challenges = get_active_challenges(user.id)

    lines = ["🎯 <b>Maqsadlar & Challengelar</b>\n"]

    if goals:
        lines.append("<b>📌 Maqsadlar:</b>")
        for g in goals:
            pct = int(g["progress"] / g["target"] * 100) if g["target"] > 0 else 0
            bar_filled = pct // 10
            bar = "🟩" * bar_filled + "⬜" * (10 - bar_filled)
            lines.append(f"  {g['title']}\n  {bar} {pct}% ({g['progress']}/{g['target']})")
    else:
        lines.append("📌 Maqsadlar yo'q.")

    if challenges:
        lines.append("\n<b>🏆 Challengelar:</b>")
        for ch in challenges:
            prog = get_challenge_progress(ch["id"])
            lines.append(f"  {ch['title']} — {prog}/{ch['duration_days']} kun")
    else:
        lines.append("\n🏆 Faol challenge yo'q.")

    text = "\n".join(lines)

    buttons = [
        [InlineKeyboardButton("➕ Yangi maqsad", callback_data="goal_add")],
        [InlineKeyboardButton("📈 Progress qo'shish", callback_data="goal_update")],
        [InlineKeyboardButton("🏆 Challenge boshlash", callback_data="ch_start")],
    ]
    if challenges:
        for ch in challenges:
            buttons.append(
                [InlineKeyboardButton(f"✅ {ch['title']} — bugun", callback_data=f"chlog_{ch['id']}")]
            )

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def goal_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("🎯 Maqsad nomini yozing (masalan: 100 ta push-up):")
    return ADDING_GOAL


async def goal_add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if len(name) > 200:
        await update.message.reply_text("❌ Nom juda uzun.")
        return ADDING_GOAL
    add_goal(update.effective_user.id, name)
    await update.message.reply_text(f"✅ <b>'{name}'</b> maqsadi qo'shildi!", parse_mode="HTML")
    return ConversationHandler.END


async def goal_update_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    goals = get_goals(q.from_user.id)
    if not goals:
        await q.message.reply_text("📌 Sizda maqsadlar yo'q.")
        return

    buttons = [
        [InlineKeyboardButton(g["title"], callback_data=f"gup_{g['id']}")]
        for g in goals
    ]
    await q.message.reply_text(
        "📈 Qaysi maqsadga progress qo'shmoqchisiz?",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def goal_update_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    goal_id = int(q.data.replace("gup_", ""))
    context.user_data["update_goal_id"] = goal_id
    await q.message.reply_text("📈 Qancha progress qo'shmoqchisiz? (son yozing):")
    return GOAL_PROGRESS


async def goal_update_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.isdigit() or int(text) <= 0:
        await update.message.reply_text("❌ Musbat son yozing.")
        return GOAL_PROGRESS
    amount = int(text)
    goal_id = context.user_data.get("update_goal_id")
    if goal_id:
        update_goal_progress(goal_id, amount)
        await update.message.reply_text(f"✅ +{amount} progress qo'shildi!")
    return ConversationHandler.END


async def ch_start_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    buttons = [
        [InlineKeyboardButton(f"{t['title']}", callback_data=f"chnew_{i}")]
        for i, t in enumerate(CHALLENGE_TEMPLATES)
    ]
    await q.message.reply_text(
        "🏆 <b>Challenge tanlang:</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def ch_new_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    idx = int(q.data.replace("chnew_", ""))
    if 0 <= idx < len(CHALLENGE_TEMPLATES):
        t = CHALLENGE_TEMPLATES[idx]
        add_challenge(q.from_user.id, t["title"], t["duration"])
        await q.message.reply_text(
            f"🏆 <b>{t['title']}</b> boshlandi!\n"
            f"📅 {t['duration']} kun | {t['desc']}",
            parse_mode="HTML",
        )


async def ch_log_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ch_id = int(q.data.replace("chlog_", ""))
    result = log_challenge_day(ch_id, q.from_user.id)
    if result:
        prog = get_challenge_progress(ch_id)
        await q.message.reply_text(f"✅ Bugun belgilandi! Progress: {prog} kun")
    else:
        await q.message.reply_text("ℹ️ Bugun allaqachon belgilangan.")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.")
    return ConversationHandler.END


def register(app):
    app.add_handler(CommandHandler("goals", goals_cmd))
    app.add_handler(CallbackQueryHandler(goal_update_start, pattern=r"^goal_update$"))
    app.add_handler(CallbackQueryHandler(ch_start_cb, pattern=r"^ch_start$"))
    app.add_handler(CallbackQueryHandler(ch_new_cb, pattern=r"^chnew_"))
    app.add_handler(CallbackQueryHandler(ch_log_cb, pattern=r"^chlog_"))

    conv_add = ConversationHandler(
        entry_points=[CallbackQueryHandler(goal_add_start, pattern=r"^goal_add$")],
        states={ADDING_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, goal_add_name)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_add)

    conv_update = ConversationHandler(
        entry_points=[CallbackQueryHandler(goal_update_select, pattern=r"^gup_")],
        states={GOAL_PROGRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, goal_update_amount)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_update)
