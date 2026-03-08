"""🛡 Anti-prokrastinatsiya handler"""
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import ensure_user
from data import EASY_TASKS, PROCRASTINATION_TIPS


async def antiprocrastination_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    text = (
        "🛡 <b>Anti-prokrastinatsiya</b>\n\n"
        "Ishni boshlash qiyinmi? Quyidagilardan birini tanlang:"
    )
    buttons = [
        [InlineKeyboardButton("⏱ 5 daqiqa challenge", callback_data="ap_5min")],
        [InlineKeyboardButton("🎯 Engil ish tanlash", callback_data="ap_easy")],
        [InlineKeyboardButton("🔨 Ishni bo'laklash", callback_data="ap_break")],
        [InlineKeyboardButton("💡 Maslahat olish", callback_data="ap_tip")],
    ]
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def ap_5min_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text(
        "⏱ <b>5 DAQIQA CHALLENGE!</b>\n\n"
        "Faqat 5 daqiqa ishlang. Timer qo'ying.\n"
        "Ko'pincha 5 daqiqadan keyin davom etasiz!\n\n"
        "⏱ Hozir boshlang! Taymerga /focus buyrug'ini ishlating.",
        parse_mode="HTML",
    )


async def ap_easy_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    task = random.choice(EASY_TASKS)
    await q.message.reply_text(
        f"🎯 <b>Eng oson ish:</b>\n\n"
        f"{task}\n\n"
        "Shuni hozir bajaring! Oddiy boshlanish — katta o'zgarish.",
        parse_mode="HTML",
    )


async def ap_break_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text(
        "🔨 <b>Ishni bo'laklash texnikasi:</b>\n\n"
        "1️⃣ Og'ir ishni yozing\n"
        "2️⃣ Uni 3-5 ta kichik qadamga bo'ling\n"
        "3️⃣ Eng birinchi qadamni hozir bajaring\n"
        "4️⃣ Har bir qadamdan keyin ✅ qo'ying\n\n"
        "Masalan:\n"
        "❌ 'Insho yozish' → og'ir\n"
        "✅ '1. Mavzu tanlash' → oson!\n"
        "✅ '2. 3 ta fikr yozish' → oson!\n"
        "✅ '3. Kirish yozish' → oson!",
        parse_mode="HTML",
    )


async def ap_tip_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    tip = random.choice(PROCRASTINATION_TIPS)
    await q.message.reply_text(f"💡 <b>Maslahat:</b>\n\n{tip}", parse_mode="HTML")


def register(app):
    app.add_handler(CommandHandler("antiprocrastination", antiprocrastination_cmd))
    app.add_handler(CallbackQueryHandler(ap_5min_cb, pattern=r"^ap_5min$"))
    app.add_handler(CallbackQueryHandler(ap_easy_cb, pattern=r"^ap_easy$"))
    app.add_handler(CallbackQueryHandler(ap_break_cb, pattern=r"^ap_break$"))
    app.add_handler(CallbackQueryHandler(ap_tip_cb, pattern=r"^ap_tip$"))
