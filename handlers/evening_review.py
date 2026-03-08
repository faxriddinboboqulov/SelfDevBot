"""🌙 Kechki tahlil handler"""
from telegram import Update
from telegram.ext import (
    ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters,
)
from database import ensure_user, save_evening_review, get_last_evening_review

WINS, MISTAKE, TOMORROW = range(3)


async def evening_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    last = get_last_evening_review(user.id)
    text = "🌙 <b>Kechki tahlil</b>\n\n"
    if last:
        text += (
            f"📅 Oxirgi tahlil: {last['date']}\n"
            f"🏆 Yutqlar: {last['wins'][:50]}...\n\n"
        )
    text += "Bugungi kunni tahlil qilamiz.\n\n🏆 Bugun nimada yutdingiz? Eng yaxshi 3 ta narsani yozing:"

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML")
    return WINS


async def get_wins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ev_wins"] = update.message.text.strip()
    await update.message.reply_text(
        "📝 Bugun qanday xato qildingiz yoki nimani yaxshilash kerak?"
    )
    return MISTAKE


async def get_mistake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ev_mistake"] = update.message.text.strip()
    await update.message.reply_text(
        "☀️ Ertaga eng muhim 1 ta ish nima bo'ladi?"
    )
    return TOMORROW


async def get_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    wins = context.user_data.get("ev_wins", "")
    mistake = context.user_data.get("ev_mistake", "")
    tomorrow = update.message.text.strip()

    save_evening_review(uid, wins, mistake, tomorrow)

    await update.message.reply_text(
        "✅ <b>Kechki tahlil saqlandi!</b>\n\n"
        f"🏆 <b>Yutqlar:</b> {wins}\n"
        f"📝 <b>Xato:</b> {mistake}\n"
        f"☀️ <b>Ertangi reja:</b> {tomorrow}\n\n"
        "Yaxshi dam oling! 🌙",
        parse_mode="HTML",
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.")
    return ConversationHandler.END


def register(app):
    conv = ConversationHandler(
        entry_points=[CommandHandler("evening", evening_cmd)],
        states={
            WINS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_wins)],
            MISTAKE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_mistake)],
            TOMORROW: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tomorrow)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
