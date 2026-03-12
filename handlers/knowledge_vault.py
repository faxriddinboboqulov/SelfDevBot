"""📂 Knowledge Vault handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters,
)
from database import ensure_user, add_knowledge, get_knowledge

CATEGORIES = ["📚 Kitob", "💡 Fikr", "🔗 Link", "📝 Eslatma", "🧠 Bilim", "💼 Ish"]
SAVING = 0


async def vault_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    text = "📂 <b>Knowledge Vault</b>\n\nKategoriya tanlang:"
    buttons = []
    for cat in CATEGORIES:
        buttons.append([
            InlineKeyboardButton(f"📖 {cat}", callback_data=f"kv_view_{cat}"),
            InlineKeyboardButton(f"➕ {cat}", callback_data=f"kv_add_{cat}"),
        ])
    buttons.append([InlineKeyboardButton("📋 Hammasi", callback_data="kv_view_all")])

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def kv_view_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cat = q.data.replace("kv_view_", "")

    if cat == "all":
        items = get_knowledge(q.from_user.id)
    else:
        items = get_knowledge(q.from_user.id, cat)

    if not items:
        await q.message.reply_text("📭 Bu kategoriyada hech narsa yo'q.")
        return

    lines = [f"📂 <b>{cat if cat != 'all' else 'Barcha yozuvlar'}:</b>\n"]
    for item in items[:15]:
        lines.append(f"🔹 [{item['category']}] {item['content'][:100]}")
    await q.message.reply_text("\n".join(lines), parse_mode="HTML")


async def kv_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cat = q.data.replace("kv_add_", "")
    context.user_data["kv_category"] = cat
    await q.message.reply_text(f"📝 <b>{cat}</b> kategoriyasiga yozuvni kiriting:", parse_mode="HTML")
    return SAVING


async def kv_add_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content = update.message.text.strip()
    if len(content) > 1000:
        await update.message.reply_text("❌ Yozuv juda uzun (max 1000 belgi).")
        return SAVING
    cat = context.user_data.get("kv_category", "📝 Eslatma")
    add_knowledge(update.effective_user.id, cat, content)
    await update.message.reply_text(f"✅ <b>{cat}</b> ga saqlandi!", parse_mode="HTML")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.")
    return ConversationHandler.END


def register(app):
    app.add_handler(CommandHandler("vault", vault_cmd))
    app.add_handler(CallbackQueryHandler(kv_view_cb, pattern=r"^kv_view_"))
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(kv_add_start, pattern=r"^kv_add_")],
        states={SAVING: [MessageHandler(filters.TEXT & ~filters.COMMAND, kv_add_content)]},
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False,
    )
    app.add_handler(conv)
