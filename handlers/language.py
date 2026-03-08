"""🌍 Til o'rganish handler"""
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import ensure_user, add_word, get_words_today, get_word_count
from data import get_daily_words, ENGLISH_WORDS


async def language_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    today_words = get_words_today(user.id)
    total = get_word_count(user.id, days=30)

    text = (
        "🌍 <b>Til o'rganish</b>\n\n"
        f"📊 Bugun: {len(today_words)} so'z | Oylik: {total} so'z\n\n"
        "Quyidagilardan tanlang:"
    )
    buttons = [
        [InlineKeyboardButton("📚 Kunlik 5 so'z", callback_data="lang_daily")],
        [InlineKeyboardButton("📝 Mini test", callback_data="lang_test")],
        [InlineKeyboardButton("🔄 Tarjima mashq", callback_data="lang_translate")],
    ]
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def lang_daily_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    words = get_daily_words(5)
    lines = ["📚 <b>Bugungi so'zlar:</b>\n"]
    for w in words:
        lines.append(f"🔹 <b>{w['en']}</b> — {w['uz']}")
        add_word(q.from_user.id, f"{w['en']} - {w['uz']}")
    lines.append(f"\n✅ {len(words)} ta so'z qo'shildi!")
    await q.message.reply_text("\n".join(lines), parse_mode="HTML")


async def lang_test_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    word = random.choice(ENGLISH_WORDS)
    wrong = random.sample([w for w in ENGLISH_WORDS if w != word], 3)
    options = [word] + wrong
    random.shuffle(options)

    context.user_data["lang_answer"] = word["uz"]
    text = f"📝 <b>'{word['en']}'</b> so'zining tarjimasi nima?\n"
    buttons = [
        [InlineKeyboardButton(o["uz"], callback_data=f"langanswer_{o['uz']}")]
        for o in options
    ]
    await q.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def lang_answer_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    selected = q.data.replace("langanswer_", "")
    correct = context.user_data.get("lang_answer", "")
    if selected == correct:
        await q.message.reply_text("✅ To'g'ri! Ajoyib!")
    else:
        await q.message.reply_text(f"❌ Noto'g'ri. To'g'ri javob: <b>{correct}</b>", parse_mode="HTML")


async def lang_translate_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    word = random.choice(ENGLISH_WORDS)
    text = (
        f"🔄 <b>Tarjima mashq</b>\n\n"
        f"🇺🇿 <b>{word['uz']}</b>\n\n"
        f"Inglizcha tarjimasi:"
    )
    buttons = [[InlineKeyboardButton("👁 Javobni ko'rish", callback_data=f"langshow_{word['en']}")]]
    await q.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def lang_show_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    en = q.data.replace("langshow_", "")
    await q.message.reply_text(f"🇬🇧 Javob: <b>{en}</b>", parse_mode="HTML")


def register(app):
    app.add_handler(CommandHandler("language", language_cmd))
    app.add_handler(CallbackQueryHandler(lang_daily_cb, pattern=r"^lang_daily$"))
    app.add_handler(CallbackQueryHandler(lang_test_cb, pattern=r"^lang_test$"))
    app.add_handler(CallbackQueryHandler(lang_answer_cb, pattern=r"^langanswer_"))
    app.add_handler(CallbackQueryHandler(lang_translate_cb, pattern=r"^lang_translate$"))
    app.add_handler(CallbackQueryHandler(lang_show_cb, pattern=r"^langshow_"))
