"""🧠 Brain training handler"""
import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import ensure_user, add_brain_score, get_brain_stats
from data import get_random_logic, get_random_math


async def brain_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    text = (
        "🧠 <b>Brain Training</b>\n\n"
        "Miyangizni mashq qiling!"
    )
    buttons = [
        [InlineKeyboardButton("🧩 Mantiqiy savol", callback_data="br_logic")],
        [InlineKeyboardButton("🔢 Tezkor matematika", callback_data="br_math")],
        [InlineKeyboardButton("📊 Natijalarim", callback_data="br_stats")],
    ]
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def br_logic_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    question = get_random_logic()
    context.user_data["br_answer"] = question["answer"]
    context.user_data["br_type"] = "logic"
    context.user_data["br_time"] = time.time()

    text = f"🧩 <b>Mantiqiy savol:</b>\n\n{question['question']}\n"
    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"brans_{opt[0]}")]
        for opt in question["options"]
    ]
    await q.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def br_math_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    question = get_random_math()
    context.user_data["br_answer"] = question["answer"]
    context.user_data["br_type"] = "math"
    context.user_data["br_time"] = time.time()

    text = f"🔢 <b>Tezkor matematika:</b>\n\n{question['question']}\n"
    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"brans_{opt[0]}")]
        for opt in question["options"]
    ]
    await q.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def br_answer_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    selected = q.data.replace("brans_", "")
    correct = context.user_data.get("br_answer", "")
    br_type = context.user_data.get("br_type", "logic")
    elapsed = round(time.time() - context.user_data.get("br_time", time.time()), 1)

    if selected == correct:
        score = max(10, 100 - int(elapsed * 5))
        add_brain_score(q.from_user.id, br_type, score)
        await q.message.reply_text(
            f"✅ To'g'ri! ⏱ {elapsed} sek | 🏆 {score} ball"
        )
    else:
        add_brain_score(q.from_user.id, br_type, 0)
        await q.message.reply_text(
            f"❌ Noto'g'ri. To'g'ri javob: <b>{correct}</b> | ⏱ {elapsed} sek",
            parse_mode="HTML",
        )


async def br_stats_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    stats = get_brain_stats(q.from_user.id)
    if not stats:
        await q.message.reply_text("📊 Hali natijalar yo'q. Savollarga javob bering!")
        return

    lines = ["📊 <b>Brain Training natijalari:</b>\n"]
    for s in stats:
        emoji = "🧩" if s["game_type"] == "logic" else "🔢"
        lines.append(
            f"{emoji} {s['game_type'].title()}: Eng yaxshi {s['best']} | "
            f"O'rtacha {round(s['avg_s'], 1)} | {s['cnt']} o'yin"
        )
    await q.message.reply_text("\n".join(lines), parse_mode="HTML")


def register(app):
    app.add_handler(CommandHandler("brain", brain_cmd))
    app.add_handler(CallbackQueryHandler(br_logic_cb, pattern=r"^br_logic$"))
    app.add_handler(CallbackQueryHandler(br_math_cb, pattern=r"^br_math$"))
    app.add_handler(CallbackQueryHandler(br_answer_cb, pattern=r"^brans_"))
    app.add_handler(CallbackQueryHandler(br_stats_cb, pattern=r"^br_stats$"))
