"""📘 Mini kurslar handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import (
    ensure_user, get_builtin_courses, add_mini_course_lesson, get_course_lessons,
)


async def course_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username, user.first_name)

    courses = get_builtin_courses()
    buttons = []
    for cid, course in courses.items():
        buttons.append(
            [InlineKeyboardButton(f"📘 {course['title']}", callback_data=f"mc_view_{cid}")]
        )
    buttons.append(
        [InlineKeyboardButton("📋 Mening kurslarim", callback_data="mc_my")]
    )

    text = (
        "📘 <b>Mini-kurslar</b>\n\n"
        "Quyidagi kurslardan birini tanlang.\n"
        "Har bir kurs qisqa darslardan iborat — offlayn o'qishingiz mumkin!"
    )
    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML")


async def course_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user = q.from_user
    data = q.data

    if data.startswith("mc_view_"):
        course_id = data[8:]
        courses = get_builtin_courses()
        if course_id not in courses:
            await q.message.reply_text("❌ Kurs topilmadi.")
            return
        course = courses[course_id]
        lines = [f"📘 <b>{course['title']}</b>\n"]
        for i, lesson in enumerate(course["lessons"], 1):
            lines.append(f"<b>📖 Dars {i}: {lesson['title']}</b>\n{lesson['content']}\n")

        buttons = [
            [InlineKeyboardButton(
                f"✅ Dars {i+1} o'qildi",
                callback_data=f"mc_done_{course_id}_{i}",
            )]
            for i in range(len(course["lessons"]))
        ]
        buttons.append(
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="mc_back")]
        )

        await q.message.reply_text(
            "\n".join(lines),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="HTML",
        )

    elif data.startswith("mc_done_"):
        parts = data.split("_")
        course_id = parts[2]
        lesson_idx = int(parts[3])
        courses = get_builtin_courses()
        if course_id in courses:
            course = courses[course_id]
            if 0 <= lesson_idx < len(course["lessons"]):
                lesson = course["lessons"][lesson_idx]
                add_mini_course_lesson(user.id, course["title"], lesson["title"])
                await q.message.reply_text(
                    f"✅ <b>{lesson['title']}</b> — dars o'qildi deb belgilandi! +5 ⭐",
                    parse_mode="HTML",
                )

    elif data == "mc_my":
        lessons = get_course_lessons(user.id)
        if not lessons:
            await q.message.reply_text("📭 Siz hali birorta darsni tugatmagansiz.")
            return
        lines = ["📋 <b>Tugatilgan darslar:</b>\n"]
        for l in lessons:
            lines.append(f"✅ {l[0]} — {l[1]} ({l[2][:10]})")
        await q.message.reply_text("\n".join(lines), parse_mode="HTML")

    elif data == "mc_back":
        await course_cmd(update, context)


def register(app):
    app.add_handler(CommandHandler("course", course_cmd))
    app.add_handler(CallbackQueryHandler(course_callback, pattern=r"^mc_"))
