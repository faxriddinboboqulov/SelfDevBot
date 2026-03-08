"""📚 Kitob tracker handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters,
)
from database import ensure_user, log_book_pages, get_book_stats

CUSTOM_PAGES = 0


async def book_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)
    stats = get_book_stats(user.id)

    text = (
        "📚 <b>Kitob o'qish tracker</b>\n\n"
        f"📆 Bu hafta: {stats['week']} sahifa\n"
        f"📅 Bu oy: {stats['month']} sahifa\n"
        f"📊 Jami: {stats['total']} sahifa\n\n"
        "O'qigan sahifalar sonini kiriting:"
    )
    buttons = [
        [
            InlineKeyboardButton("📖 5", callback_data="book_5"),
            InlineKeyboardButton("📖 10", callback_data="book_10"),
            InlineKeyboardButton("📖 20", callback_data="book_20"),
        ],
        [
            InlineKeyboardButton("📖 30", callback_data="book_30"),
            InlineKeyboardButton("📖 50", callback_data="book_50"),
            InlineKeyboardButton("📖 100", callback_data="book_100"),
        ],
        [InlineKeyboardButton("✏️ Boshqa son kiritish", callback_data="book_custom")],
    ]
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def book_quick_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    pages = int(q.data.replace("book_", ""))
    log_book_pages(q.from_user.id, pages)
    await q.message.reply_text(f"✅ {pages} sahifa qo'shildi! 📚")


async def book_custom_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("📝 Sahifalar sonini yozing (masalan: 45):")
    return CUSTOM_PAGES


async def book_custom_pages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.isdigit() or int(text) <= 0 or int(text) > 10000:
        await update.message.reply_text("❌ Iltimos, 1-10000 orasida son yozing.")
        return CUSTOM_PAGES
    pages = int(text)
    log_book_pages(update.effective_user.id, pages)
    await update.message.reply_text(f"✅ {pages} sahifa qo'shildi! 📚")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.")
    return ConversationHandler.END


def register(app):
    app.add_handler(CommandHandler("book", book_cmd))
    app.add_handler(CallbackQueryHandler(book_quick_cb, pattern=r"^book_\d+$"))
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(book_custom_start, pattern=r"^book_custom$")],
        states={
            CUSTOM_PAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, book_custom_pages)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
