"""💡 Shaxsiy tavsiyalar handler"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import (
    ensure_user, get_full_stats, get_book_stats, get_focus_stats,
    get_mood_averages, get_non_zero_streak, get_total_score,
)
from handlers.score_system import get_level


async def recommend_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    s7 = get_full_stats(user.id, days=7)
    book = get_book_stats(user.id)
    focus = get_focus_stats(user.id, days=7)
    mood = get_mood_averages(user.id, days=7)
    streak = get_non_zero_streak(user.id)
    total_score = get_total_score(user.id)
    level_name, _ = get_level(total_score)

    tips = []

    # Sport tahlili
    if s7["workouts"] >= 5:
        tips.append("💪 <b>Sport — ajoyib!</b> Haftalik sportingiz zo'r. Shu darajada davom eting!")
    elif s7["workouts"] >= 3:
        tips.append("💪 <b>Sport — yaxshi.</b> Yana 1-2 kun qo'shing va mukammal bo'ladi!")
    else:
        tips.append("🏃 <b>Sport — sustlashgan!</b> Bu hafta kam sport qildingiz. Ertaga albatta trenirovka qiling!")

    # Kitob tahlili
    if book["week"] >= 50:
        tips.append("📚 <b>Kitob — ajoyib!</b> Haftalik o'qish juda yaxshi!")
    elif book["week"] >= 20:
        tips.append("📚 <b>Kitob — yaxshi.</b> Yana biroz ko'proq o'qing!")
    else:
        tips.append("📚 <b>Kitob — sustlashgan!</b> Bu hafta kam o'qigansiz. Ertaga kitobga e'tibor bering!")

    # Til tahlili
    if s7["words"] >= 25:
        tips.append("🌍 <b>Til — ajoyib!</b> So'z o'rganish yaxshi ketayapti!")
    elif s7["words"] >= 10:
        tips.append("🌍 <b>Til — yaxshi.</b> Yana biroz ko'proq so'z o'rganing!")
    else:
        tips.append("🌍 <b>Til — sustlashgan!</b> Har kuni 5 ta so'z o'rganishni unutmang!")

    # Focus tahlili
    if focus["total_minutes"] >= 150:
        tips.append("🎯 <b>Focus — ajoyib!</b> Diqqatingiz zo'r!")
    elif focus["total_minutes"] >= 60:
        tips.append("🎯 <b>Focus — yaxshi.</b> Focus sessiyalarni ko'paytiring!")
    else:
        tips.append("🎯 <b>Focus — sustlashgan!</b> Har kuni kamida 1 ta Pomodoro qiling!")

    # Kayfiyat bo'yicha maslahat
    if mood["count"] > 0:
        if mood["avg_mood"] < 3:
            tips.append("😊 <b>Kayfiyat past.</b> Sport, tabiat va ijobiy odamlar kayfiyatni ko'taradi!")
        if mood["avg_stress"] > 3.5:
            tips.append("🧘 <b>Stress yuqori.</b> Meditatsiya, dam olish va yurish tavsiya etiladi!")
        if mood["avg_energy"] < 3:
            tips.append("⚡ <b>Energiya past.</b> Yaxshi uxlang, suv iching va sport qiling!")

    # Streak
    if streak >= 7:
        tips.append(f"🔥 <b>{streak} kunlik streak!</b> Ajoyib! Buzmang!")
    elif streak == 0:
        tips.append("🚨 <b>Streak 0!</b> Bugun bitta foydali ish qiling va streakni boshlang!")

    # Eng zaif yo'nalish
    weakest = min(
        [("Sport", s7["workouts"]), ("Kitob", book["week"]), ("Til", s7["words"])],
        key=lambda x: x[1],
    )
    tips.append(f"\n📈 <b>Ertangi urg'u:</b> {weakest[0]} — bunga ko'proq vaqt ajrating!")

    text = (
        f"💡 <b>Shaxsiy tavsiyalar</b>\n"
        f"🏅 Daraja: {level_name} | ⭐ {total_score} ball\n\n"
        + "\n\n".join(tips)
    )

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, parse_mode="HTML")


def register(app):
    app.add_handler(CommandHandler("recommend", recommend_cmd))
