"""⚡ Tez yozuv (Quick Log) handler"""
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import (
    ensure_user, log_book_pages, log_workout, add_focus_session, add_word, add_score,
    check_and_unlock_achievements,
)
from data import get_celebration, ACHIEVEMENTS


async def quicklog_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    text = (
        "⚡ <b>Tez yozuv</b>\n\n"
        "1 tugma bosish bilan yozing!"
    )
    buttons = [
        [
            InlineKeyboardButton("📖 +5 sahifa", callback_data="ql_book5"),
            InlineKeyboardButton("📖 +10 sahifa", callback_data="ql_book10"),
        ],
        [
            InlineKeyboardButton("📖 +20 sahifa", callback_data="ql_book20"),
            InlineKeyboardButton("📖 +50 sahifa", callback_data="ql_book50"),
        ],
        [
            InlineKeyboardButton("💪 +1 trenirovka", callback_data="ql_workout"),
            InlineKeyboardButton("🎯 +1 focus (25min)", callback_data="ql_focus"),
        ],
        [
            InlineKeyboardButton("🌍 +5 so'z", callback_data="ql_words"),
        ],
    ]
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def ql_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    data = q.data

    c = get_celebration()
    if data == "ql_book5":
        log_book_pages(uid, 5)
        add_score(uid, "book", 3, "Quick log 5p")
        await q.message.reply_text(f"✅ +5 sahifa qo'shildi! +3 ⭐\n\n{c}")
    elif data == "ql_book10":
        log_book_pages(uid, 10)
        add_score(uid, "book", 5, "Quick log 10p")
        await q.message.reply_text(f"✅ +10 sahifa qo'shildi! +5 ⭐\n\n{c}")
    elif data == "ql_book20":
        log_book_pages(uid, 20)
        add_score(uid, "book", 8, "Quick log 20p")
        await q.message.reply_text(f"✅ +20 sahifa qo'shildi! +8 ⭐\n\n{c}")
    elif data == "ql_book50":
        log_book_pages(uid, 50)
        add_score(uid, "book", 12, "Quick log 50p")
        await q.message.reply_text(f"🎉🎉 +50 sahifa! KUCHLI! +12 ⭐\n\n{c}")
    elif data == "ql_workout":
        log_workout(uid, "Quick trenirovka", "Quick")
        add_score(uid, "workout", 10, "Quick log workout")
        await q.message.reply_text(f"💪 Trenirovka yozildi! +10 ⭐\n\n{c}")
    elif data == "ql_focus":
        add_focus_session(uid, 25)
        add_score(uid, "focus", 6, "Quick log focus")
        await q.message.reply_text(f"🎯 25 min focus yozildi! +6 ⭐\n\n{c}")
    elif data == "ql_words":
        words = ["hello-salom", "good-yaxshi", "learn-o'rganmoq", "read-o'qimoq", "write-yozmoq"]
        for w in words:
            add_word(uid, w)
        add_score(uid, "language", 7, "Quick log 5 words")
        await q.message.reply_text(f"🌍 5 ta so'z qo'shildi! +7 ⭐\n\n{c}")

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
    app.add_handler(CommandHandler("quicklog", quicklog_cmd))
    app.add_handler(CallbackQueryHandler(ql_callback, pattern=r"^ql_"))
