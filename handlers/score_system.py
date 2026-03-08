"""⭐ Ball tizimi handler"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import (
    ensure_user, get_total_score, get_score_today, get_score_breakdown,
    add_score, get_all_users, get_full_stats,
)

SCORE_MAP = {
    "workout": 10,
    "book": 8,
    "language": 7,
    "focus": 6,
    "habit": 5,
    "brain": 5,
    "mood": 3,
    "evening": 5,
    "video": 3,
}

LEVELS = [
    (0, "🌱 Yangi boshlovchi"),
    (50, "🌿 Boshlang'ich"),
    (150, "🌳 O'rta daraja"),
    (400, "⭐ Yaxshi"),
    (800, "🏆 Zo'r"),
    (1500, "👑 Usta"),
    (3000, "🔥 Legenda"),
]

PENALTY_MAP = {
    "no_workout": -3,
    "no_book": -2,
    "no_language": -2,
    "zero_day": -5,
}


def get_level(total_score):
    level_name = LEVELS[0][1]
    next_threshold = LEVELS[1][0] if len(LEVELS) > 1 else None
    for i, (threshold, name) in enumerate(LEVELS):
        if total_score >= threshold:
            level_name = name
            next_threshold = LEVELS[i + 1][0] if i + 1 < len(LEVELS) else None
    return level_name, next_threshold


async def score_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    total = get_total_score(user.id)
    today = get_score_today(user.id)
    breakdown = get_score_breakdown(user.id, 7)
    level_name, next_thresh = get_level(total)

    lines = [
        f"⭐ <b>Ball tizimi</b>\n",
        f"🏅 Daraja: {level_name}",
        f"⭐ Jami: {total} ball",
        f"📅 Bugun: +{today} ball",
    ]

    if next_thresh:
        remaining = next_thresh - total
        lines.append(f"📈 Keyingi daraja: yana {remaining} ball kerak")

    if breakdown:
        lines.append("\n📊 <b>7 kunlik taqsimot:</b>")
        for item in breakdown:
            lines.append(f"  • {item['category']}: {item['total']} ball")

    lines.append(
        "\n<b>Ball qoidalari:</b>\n"
        "💪 Sport: +10 | 📚 Kitob: +8 | 🌍 Til: +7\n"
        "🎯 Focus: +6 | 🔥 Odat: +5 | 🧠 Brain: +5\n"
        "😊 Kayfiyat: +3 | 🌙 Tahlil: +5 | 🎥 Video: +3\n\n"
        "<b>Jarima:</b>\n"
        "❌ Sport yo'q: -3 | ❌ Kitob yo'q: -2\n"
        "❌ Til yo'q: -2 | ❌ Zero day: -5"
    )

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text("\n".join(lines), parse_mode="HTML")


async def check_daily_penalties(context: ContextTypes.DEFAULT_TYPE):
    """Job queue orqali kechqurun jarima tekshiruvi"""
    users = get_all_users()
    for uid in users:
        try:
            stats = get_full_stats(uid, days=1)
            penalties = []
            if stats["workouts"] == 0:
                add_score(uid, "penalty", PENALTY_MAP["no_workout"], "Sport qilinmadi")
                penalties.append("sport")
            if stats["pages"] == 0:
                add_score(uid, "penalty", PENALTY_MAP["no_book"], "Kitob o'qilmadi")
                penalties.append("kitob")
            if stats["words"] == 0:
                add_score(uid, "penalty", PENALTY_MAP["no_language"], "So'z o'rganilmadi")
                penalties.append("til")
            if penalties:
                text = (
                    "⚠️ <b>Kunlik jarima!</b>\n\n"
                    f"Bu kategoriyalarda ish qilinmadi: {', '.join(penalties)}\n"
                    "Ertaga albatta bajaring!"
                )
                await context.bot.send_message(uid, text, parse_mode="HTML")
        except Exception:
            pass


def register(app):
    app.add_handler(CommandHandler("score", score_cmd))
