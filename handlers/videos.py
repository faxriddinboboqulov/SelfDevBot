"""🎥 Foydali videolar handler"""
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import ensure_user, log_video
from data import VIDEOS, get_random_video


async def videos_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    text = "🎥 <b>Foydali videolar</b>\n\nKategoriya tanlang:"
    buttons = []
    for cat in VIDEOS:
        buttons.append([InlineKeyboardButton(f"🎬 {cat}", callback_data=f"vidcat_{cat}")])
    buttons.append([InlineKeyboardButton("🎲 Tasodifiy video", callback_data="vid_random")])

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def vid_category_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cat = q.data.replace("vidcat_", "")
    vids = VIDEOS.get(cat, [])
    if not vids:
        await q.message.reply_text("❌ Bu kategoriyada video topilmadi.")
        return

    lines = [f"🎬 <b>{cat}:</b>\n"]
    buttons = []
    for i, v in enumerate(vids):
        lines.append(f"🔹 {v['title']}")
        buttons.append(
            [InlineKeyboardButton(f"▶️ {v['title']}", callback_data=f"vidwatch_{cat}_{i}")]
        )

    await q.message.reply_text(
        "\n".join(lines), parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons)
    )


async def vid_watch_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    parts = q.data.replace("vidwatch_", "").rsplit("_", 1)
    cat = parts[0]
    idx = int(parts[1])
    vids = VIDEOS.get(cat, [])
    if 0 <= idx < len(vids):
        v = vids[idx]
        log_video(q.from_user.id, cat, v["title"])
        await q.message.reply_text(
            f"▶️ <b>{v['title']}</b>\n\n🔗 {v['url']}",
            parse_mode="HTML",
        )


async def vid_random_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    v = get_random_video()
    if v:
        await q.message.reply_text(
            f"🎲 <b>{v['title']}</b>\n\n🔗 {v['url']}",
            parse_mode="HTML",
        )


def register(app):
    app.add_handler(CommandHandler("videos", videos_cmd))
    app.add_handler(CallbackQueryHandler(vid_category_cb, pattern=r"^vidcat_"))
    app.add_handler(CallbackQueryHandler(vid_watch_cb, pattern=r"^vidwatch_"))
    app.add_handler(CallbackQueryHandler(vid_random_cb, pattern=r"^vid_random$"))
