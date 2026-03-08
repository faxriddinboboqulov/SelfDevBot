"""😊 Kayfiyat tracker handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import ensure_user, log_mood, get_mood_averages


async def mood_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    text = "😊 <b>Kayfiyat tracker</b>\n\nBugungi kayfiyatingiz qanday? (1-5)"
    buttons = [
        [
            InlineKeyboardButton("😢 1", callback_data="mood_m_1"),
            InlineKeyboardButton("😕 2", callback_data="mood_m_2"),
            InlineKeyboardButton("😐 3", callback_data="mood_m_3"),
            InlineKeyboardButton("🙂 4", callback_data="mood_m_4"),
            InlineKeyboardButton("😄 5", callback_data="mood_m_5"),
        ]
    ]
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def mood_step1_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    mood = int(q.data.split("_")[-1])
    context.user_data["mood_val"] = mood

    text = "⚡ Energiya darajangiz? (1-5)"
    buttons = [
        [
            InlineKeyboardButton("😴 1", callback_data="mood_e_1"),
            InlineKeyboardButton("🥱 2", callback_data="mood_e_2"),
            InlineKeyboardButton("😐 3", callback_data="mood_e_3"),
            InlineKeyboardButton("💪 4", callback_data="mood_e_4"),
            InlineKeyboardButton("🔥 5", callback_data="mood_e_5"),
        ]
    ]
    await q.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def mood_step2_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    energy = int(q.data.split("_")[-1])
    context.user_data["energy_val"] = energy

    text = "🧘 Stress darajangiz? (1-5, 1=past, 5=yuqori)"
    buttons = [
        [
            InlineKeyboardButton("🧘 1", callback_data="mood_s_1"),
            InlineKeyboardButton("😌 2", callback_data="mood_s_2"),
            InlineKeyboardButton("😐 3", callback_data="mood_s_3"),
            InlineKeyboardButton("😰 4", callback_data="mood_s_4"),
            InlineKeyboardButton("🤯 5", callback_data="mood_s_5"),
        ]
    ]
    await q.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def mood_step3_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    stress = int(q.data.split("_")[-1])
    mood = context.user_data.get("mood_val", 3)
    energy = context.user_data.get("energy_val", 3)

    log_mood(uid, mood, energy, stress)
    avgs = get_mood_averages(uid, 7)

    text = (
        "✅ <b>Kayfiyat saqlandi!</b>\n\n"
        f"😊 Kayfiyat: {mood}/5\n"
        f"⚡ Energiya: {energy}/5\n"
        f"🧘 Stress: {stress}/5\n\n"
        f"📊 <b>7 kunlik o'rtacha:</b>\n"
        f"😊 Kayfiyat: {avgs['avg_mood']}\n"
        f"⚡ Energiya: {avgs['avg_energy']}\n"
        f"🧘 Stress: {avgs['avg_stress']}"
    )
    await q.message.reply_text(text, parse_mode="HTML")


def register(app):
    app.add_handler(CommandHandler("mood", mood_cmd))
    app.add_handler(CallbackQueryHandler(mood_step1_cb, pattern=r"^mood_m_\d$"))
    app.add_handler(CallbackQueryHandler(mood_step2_cb, pattern=r"^mood_e_\d$"))
    app.add_handler(CallbackQueryHandler(mood_step3_cb, pattern=r"^mood_s_\d$"))
