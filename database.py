"""🗄️ Ma'lumotlar bazasi — barcha jadvallar va CRUD funksiyalar"""
import sqlite3
import os
from datetime import datetime, timedelta
import pytz

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "selfdev.db")
TZ = pytz.timezone("Asia/Tashkent")


def _now():
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def _today():
    return datetime.now(TZ).strftime("%Y-%m-%d")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


# ══════════════════════════════════════════
#  JADVALLAR YARATISH
# ══════════════════════════════════════════
def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        joined_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS daily_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        is_done INTEGER DEFAULT 0,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS habit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        user_id INTEGER,
        date TEXT,
        FOREIGN KEY(habit_id) REFERENCES habits(id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS workout_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        workout_name TEXT,
        level TEXT,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS word_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        word TEXT,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS book_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        pages INTEGER,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS video_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        title TEXT,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        target INTEGER DEFAULT 100,
        progress INTEGER DEFAULT 0,
        is_done INTEGER DEFAULT 0,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        duration_days INTEGER,
        start_date TEXT,
        is_active INTEGER DEFAULT 1,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS challenge_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        challenge_id INTEGER,
        user_id INTEGER,
        date TEXT,
        FOREIGN KEY(challenge_id) REFERENCES challenges(id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        content TEXT,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        text TEXT,
        remind_time TEXT,
        is_sent INTEGER DEFAULT 0,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS focus_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        minutes INTEGER,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS brain_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        game_type TEXT,
        score INTEGER,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS mood_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        mood INTEGER,
        energy INTEGER,
        stress INTEGER,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS evening_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        wins TEXT,
        mistake TEXT,
        tomorrow TEXT,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS score_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        points INTEGER,
        reason TEXT,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS mini_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        course_name TEXT,
        lesson_title TEXT,
        completed_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")

    conn.commit()
    conn.close()


# ══════════════════════════════════════════
#  FOYDALANUVCHI
# ══════════════════════════════════════════
def ensure_user(user_id, username=None, first_name=None):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    if not c.fetchone():
        c.execute("INSERT INTO users(user_id,username,first_name,joined_at) VALUES(?,?,?,?)",
                  (user_id, username, first_name, _now()))
    conn.commit()
    conn.close()


def get_all_users():
    conn = get_conn()
    rows = conn.execute("SELECT user_id FROM users").fetchall()
    conn.close()
    return [r["user_id"] for r in rows]


# ══════════════════════════════════════════
#  KUNLIK REJA
# ══════════════════════════════════════════
DEFAULT_TASKS = [
    "📚 30 daqiqa kitob o'qish",
    "💪 Trenirovka qilish",
    "🌍 5 ta yangi so'z o'rganish",
    "🧘 10 daqiqa meditatsiya",
    "📝 Kunlik yozuv",
]


def seed_default_daily_tasks(user_id):
    conn = get_conn()
    today = _today()
    c = conn.cursor()
    c.execute("SELECT id FROM daily_tasks WHERE user_id=? AND date=?", (user_id, today))
    if not c.fetchone():
        for t in DEFAULT_TASKS:
            c.execute("INSERT INTO daily_tasks(user_id,title,is_done,date) VALUES(?,?,0,?)",
                      (user_id, t, today))
        conn.commit()
    conn.close()


def get_daily_tasks(user_id):
    conn = get_conn()
    today = _today()
    rows = conn.execute(
        "SELECT id,title,is_done FROM daily_tasks WHERE user_id=? AND date=?",
        (user_id, today),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def toggle_task(task_id, user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT is_done FROM daily_tasks WHERE id=? AND user_id=?", (task_id, user_id))
    row = c.fetchone()
    if row:
        new_val = 0 if row["is_done"] else 1
        c.execute("UPDATE daily_tasks SET is_done=? WHERE id=?", (new_val, task_id))
        conn.commit()
    conn.close()


# ══════════════════════════════════════════
#  ODATLAR
# ══════════════════════════════════════════
def add_habit(user_id, name):
    conn = get_conn()
    conn.execute("INSERT INTO habits(user_id,name,created_at) VALUES(?,?,?)",
                 (user_id, name, _now()))
    conn.commit()
    conn.close()


def get_habits(user_id):
    conn = get_conn()
    rows = conn.execute("SELECT id,name FROM habits WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def log_habit(habit_id, user_id):
    conn = get_conn()
    today = _today()
    c = conn.cursor()
    c.execute("SELECT id FROM habit_logs WHERE habit_id=? AND user_id=? AND date=?",
              (habit_id, user_id, today))
    if not c.fetchone():
        c.execute("INSERT INTO habit_logs(habit_id,user_id,date) VALUES(?,?,?)",
                  (habit_id, user_id, today))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False


def get_habit_streak(habit_id, user_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT DISTINCT date FROM habit_logs WHERE habit_id=? AND user_id=? ORDER BY date DESC",
        (habit_id, user_id),
    ).fetchall()
    conn.close()
    if not rows:
        return 0
    streak = 0
    today = datetime.now(TZ).date()
    for r in rows:
        expected = today - timedelta(days=streak)
        if r["date"] == expected.strftime("%Y-%m-%d"):
            streak += 1
        else:
            break
    return streak


def is_habit_done_today(habit_id, user_id):
    conn = get_conn()
    today = _today()
    row = conn.execute(
        "SELECT id FROM habit_logs WHERE habit_id=? AND user_id=? AND date=?",
        (habit_id, user_id, today),
    ).fetchone()
    conn.close()
    return row is not None


# ══════════════════════════════════════════
#  SPORT
# ══════════════════════════════════════════
def log_workout(user_id, workout_name, level):
    conn = get_conn()
    conn.execute("INSERT INTO workout_logs(user_id,workout_name,level,date) VALUES(?,?,?,?)",
                 (user_id, workout_name, level, _today()))
    conn.commit()
    conn.close()


def get_workout_count(user_id, days=7):
    conn = get_conn()
    since = (datetime.now(TZ) - timedelta(days=days)).strftime("%Y-%m-%d")
    row = conn.execute(
        "SELECT COUNT(*) as cnt FROM workout_logs WHERE user_id=? AND date>=?",
        (user_id, since),
    ).fetchone()
    conn.close()
    return row["cnt"] if row else 0


# ══════════════════════════════════════════
#  TIL O'RGANISH
# ══════════════════════════════════════════
def add_word(user_id, word):
    conn = get_conn()
    conn.execute("INSERT INTO word_logs(user_id,word,date) VALUES(?,?,?)",
                 (user_id, word, _today()))
    conn.commit()
    conn.close()


def get_word_count(user_id, days=7):
    conn = get_conn()
    since = (datetime.now(TZ) - timedelta(days=days)).strftime("%Y-%m-%d")
    row = conn.execute(
        "SELECT COUNT(*) as cnt FROM word_logs WHERE user_id=? AND date>=?",
        (user_id, since),
    ).fetchone()
    conn.close()
    return row["cnt"] if row else 0


def get_words_today(user_id):
    conn = get_conn()
    today = _today()
    rows = conn.execute(
        "SELECT word FROM word_logs WHERE user_id=? AND date=?",
        (user_id, today),
    ).fetchall()
    conn.close()
    return [r["word"] for r in rows]


# ══════════════════════════════════════════
#  KITOB
# ══════════════════════════════════════════
def log_book_pages(user_id, pages):
    conn = get_conn()
    conn.execute("INSERT INTO book_logs(user_id,pages,date) VALUES(?,?,?)",
                 (user_id, pages, _today()))
    conn.commit()
    conn.close()


def get_book_stats(user_id):
    conn = get_conn()
    today = datetime.now(TZ)
    week_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    month_ago = (today - timedelta(days=30)).strftime("%Y-%m-%d")

    w = conn.execute(
        "SELECT COALESCE(SUM(pages),0) as s FROM book_logs WHERE user_id=? AND date>=?",
        (user_id, week_ago),
    ).fetchone()
    m = conn.execute(
        "SELECT COALESCE(SUM(pages),0) as s FROM book_logs WHERE user_id=? AND date>=?",
        (user_id, month_ago),
    ).fetchone()
    t = conn.execute(
        "SELECT COALESCE(SUM(pages),0) as s FROM book_logs WHERE user_id=?",
        (user_id,),
    ).fetchone()
    conn.close()
    return {"week": w["s"], "month": m["s"], "total": t["s"]}


# ══════════════════════════════════════════
#  VIDEOLAR
# ══════════════════════════════════════════
def log_video(user_id, category, title):
    conn = get_conn()
    conn.execute("INSERT INTO video_logs(user_id,category,title,date) VALUES(?,?,?,?)",
                 (user_id, category, title, _today()))
    conn.commit()
    conn.close()


# ══════════════════════════════════════════
#  MAQSADLAR
# ══════════════════════════════════════════
def add_goal(user_id, title, target=100):
    conn = get_conn()
    conn.execute("INSERT INTO goals(user_id,title,target,progress,is_done,created_at) VALUES(?,?,?,0,0,?)",
                 (user_id, title, target, _now()))
    conn.commit()
    conn.close()


def get_goals(user_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id,title,target,progress,is_done FROM goals WHERE user_id=? AND is_done=0",
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_goal_progress(goal_id, amount):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT target,progress FROM goals WHERE id=?", (goal_id,))
    row = c.fetchone()
    if row:
        new_prog = min(row["target"], row["progress"] + amount)
        is_done = 1 if new_prog >= row["target"] else 0
        c.execute("UPDATE goals SET progress=?,is_done=? WHERE id=?", (new_prog, is_done, goal_id))
        conn.commit()
    conn.close()


# CHALLENGES
def add_challenge(user_id, title, duration_days):
    conn = get_conn()
    conn.execute("INSERT INTO challenges(user_id,title,duration_days,start_date,is_active) VALUES(?,?,?,?,1)",
                 (user_id, title, duration_days, _today()))
    conn.commit()
    conn.close()


def get_active_challenges(user_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id,title,duration_days,start_date FROM challenges WHERE user_id=? AND is_active=1",
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def log_challenge_day(challenge_id, user_id):
    conn = get_conn()
    today = _today()
    c = conn.cursor()
    c.execute("SELECT id FROM challenge_logs WHERE challenge_id=? AND user_id=? AND date=?",
              (challenge_id, user_id, today))
    if not c.fetchone():
        c.execute("INSERT INTO challenge_logs(challenge_id,user_id,date) VALUES(?,?,?)",
                  (challenge_id, user_id, today))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False


def get_challenge_progress(challenge_id):
    conn = get_conn()
    row = conn.execute(
        "SELECT COUNT(*) as cnt FROM challenge_logs WHERE challenge_id=?",
        (challenge_id,),
    ).fetchone()
    conn.close()
    return row["cnt"] if row else 0


# ══════════════════════════════════════════
#  KNOWLEDGE VAULT
# ══════════════════════════════════════════
def add_knowledge(user_id, category, content):
    conn = get_conn()
    conn.execute("INSERT INTO knowledge(user_id,category,content,date) VALUES(?,?,?,?)",
                 (user_id, category, content, _now()))
    conn.commit()
    conn.close()


def get_knowledge(user_id, category=None):
    conn = get_conn()
    if category:
        rows = conn.execute(
            "SELECT id,category,content,date FROM knowledge WHERE user_id=? AND category=? ORDER BY date DESC LIMIT 20",
            (user_id, category),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id,category,content,date FROM knowledge WHERE user_id=? ORDER BY date DESC LIMIT 20",
            (user_id,),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ══════════════════════════════════════════
#  ESLATMALAR
# ══════════════════════════════════════════
def add_reminder(user_id, text, remind_time):
    conn = get_conn()
    conn.execute("INSERT INTO reminders(user_id,text,remind_time,is_sent,date) VALUES(?,?,?,0,?)",
                 (user_id, text, remind_time, _today()))
    conn.commit()
    conn.close()


def get_pending_reminders():
    conn = get_conn()
    now = datetime.now(TZ).strftime("%H:%M")
    today = _today()
    rows = conn.execute(
        "SELECT id,user_id,text,remind_time FROM reminders WHERE is_sent=0 AND date=? AND remind_time<=?",
        (today, now),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_reminder_sent(reminder_id):
    conn = get_conn()
    conn.execute("UPDATE reminders SET is_sent=1 WHERE id=?", (reminder_id,))
    conn.commit()
    conn.close()


def get_user_reminders(user_id):
    conn = get_conn()
    today = _today()
    rows = conn.execute(
        "SELECT id,text,remind_time,is_sent FROM reminders WHERE user_id=? AND date=? ORDER BY remind_time",
        (user_id, today),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ══════════════════════════════════════════
#  FOCUS TIMER
# ══════════════════════════════════════════
def add_focus_session(user_id, minutes):
    conn = get_conn()
    conn.execute("INSERT INTO focus_sessions(user_id,minutes,date) VALUES(?,?,?)",
                 (user_id, minutes, _today()))
    conn.commit()
    conn.close()


def get_focus_stats(user_id, days=7):
    conn = get_conn()
    since = (datetime.now(TZ) - timedelta(days=days)).strftime("%Y-%m-%d")
    row = conn.execute(
        "SELECT COALESCE(SUM(minutes),0) as total, COUNT(*) as cnt FROM focus_sessions WHERE user_id=? AND date>=?",
        (user_id, since),
    ).fetchone()
    conn.close()
    return {"total_minutes": row["total"], "sessions": row["cnt"]}


# ══════════════════════════════════════════
#  BRAIN TRAINING
# ══════════════════════════════════════════
def add_brain_score(user_id, game_type, score):
    conn = get_conn()
    conn.execute("INSERT INTO brain_scores(user_id,game_type,score,date) VALUES(?,?,?,?)",
                 (user_id, game_type, score, _today()))
    conn.commit()
    conn.close()


def get_brain_stats(user_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT game_type, MAX(score) as best, AVG(score) as avg_s, COUNT(*) as cnt "
        "FROM brain_scores WHERE user_id=? GROUP BY game_type",
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ══════════════════════════════════════════
#  UMUMIY STATISTIKA
# ══════════════════════════════════════════
def get_full_stats(user_id, days=30):
    conn = get_conn()
    since = (datetime.now(TZ) - timedelta(days=days)).strftime("%Y-%m-%d")
    w = conn.execute("SELECT COUNT(*) as c FROM workout_logs WHERE user_id=? AND date>=?",
                     (user_id, since)).fetchone()["c"]
    wo = conn.execute("SELECT COUNT(*) as c FROM word_logs WHERE user_id=? AND date>=?",
                      (user_id, since)).fetchone()["c"]
    b = conn.execute("SELECT COALESCE(SUM(pages),0) as c FROM book_logs WHERE user_id=? AND date>=?",
                     (user_id, since)).fetchone()["c"]
    v = conn.execute("SELECT COUNT(*) as c FROM video_logs WHERE user_id=? AND date>=?",
                     (user_id, since)).fetchone()["c"]
    f = conn.execute("SELECT COALESCE(SUM(minutes),0) as c FROM focus_sessions WHERE user_id=? AND date>=?",
                     (user_id, since)).fetchone()["c"]
    h = conn.execute(
        "SELECT COUNT(DISTINCT date) as c FROM habit_logs WHERE user_id=? AND date>=?",
        (user_id, since),
    ).fetchone()["c"]
    conn.close()
    return {
        "workouts": w, "words": wo, "pages": b,
        "videos": v, "focus_min": f, "habit_days": h,
    }


# ══════════════════════════════════════════
#  KAYFIYAT TRACKER
# ══════════════════════════════════════════
def log_mood(user_id, mood, energy, stress):
    conn = get_conn()
    conn.execute("INSERT INTO mood_logs(user_id,mood,energy,stress,date) VALUES(?,?,?,?,?)",
                 (user_id, mood, energy, stress, _today()))
    conn.commit()
    conn.close()


def get_mood_averages(user_id, days=7):
    conn = get_conn()
    since = (datetime.now(TZ) - timedelta(days=days)).strftime("%Y-%m-%d")
    row = conn.execute(
        "SELECT AVG(mood) as avg_mood, AVG(energy) as avg_energy, AVG(stress) as avg_stress, COUNT(*) as cnt "
        "FROM mood_logs WHERE user_id=? AND date>=?",
        (user_id, since),
    ).fetchone()
    conn.close()
    return {
        "avg_mood": round(row["avg_mood"] or 0, 1),
        "avg_energy": round(row["avg_energy"] or 0, 1),
        "avg_stress": round(row["avg_stress"] or 0, 1),
        "count": row["cnt"],
    }


# ══════════════════════════════════════════
#  KECHKI TAHLIL
# ══════════════════════════════════════════
def save_evening_review(user_id, wins, mistake, tomorrow):
    conn = get_conn()
    conn.execute(
        "INSERT INTO evening_reviews(user_id,wins,mistake,tomorrow,date) VALUES(?,?,?,?,?)",
        (user_id, wins, mistake, tomorrow, _today()),
    )
    conn.commit()
    conn.close()


def get_last_evening_review(user_id):
    conn = get_conn()
    row = conn.execute(
        "SELECT wins,mistake,tomorrow,date FROM evening_reviews WHERE user_id=? ORDER BY id DESC LIMIT 1",
        (user_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ══════════════════════════════════════════
#  BALL TIZIMI
# ══════════════════════════════════════════
def add_score(user_id, category, points, reason=""):
    conn = get_conn()
    conn.execute(
        "INSERT INTO score_logs(user_id,category,points,reason,date) VALUES(?,?,?,?,?)",
        (user_id, category, points, reason, _today()),
    )
    conn.commit()
    conn.close()


def get_total_score(user_id):
    conn = get_conn()
    row = conn.execute(
        "SELECT COALESCE(SUM(points),0) as total FROM score_logs WHERE user_id=?",
        (user_id,),
    ).fetchone()
    conn.close()
    return row["total"]


def get_score_today(user_id):
    conn = get_conn()
    today = _today()
    row = conn.execute(
        "SELECT COALESCE(SUM(points),0) as total FROM score_logs WHERE user_id=? AND date=?",
        (user_id, today),
    ).fetchone()
    conn.close()
    return row["total"]


def get_score_breakdown(user_id, days=7):
    conn = get_conn()
    since = (datetime.now(TZ) - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = conn.execute(
        "SELECT category, SUM(points) as total FROM score_logs WHERE user_id=? AND date>=? GROUP BY category ORDER BY total DESC",
        (user_id, since),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ══════════════════════════════════════════
#  NO ZERO DAY
# ══════════════════════════════════════════
def is_zero_day(user_id):
    """Bugun birorta foydali ish qilinganmi?"""
    conn = get_conn()
    today = _today()
    checks = [
        ("workout_logs", "date"),
        ("book_logs", "date"),
        ("word_logs", "date"),
        ("focus_sessions", "date"),
        ("habit_logs", "date"),
        ("brain_scores", "date"),
    ]
    for table, col in checks:
        row = conn.execute(
            f"SELECT id FROM {table} WHERE user_id=? AND {col}=? LIMIT 1",
            (user_id, today),
        ).fetchone()
        if row:
            conn.close()
            return False  # Birorta ish qilingan — zero emas
    conn.close()
    return True  # Hech narsa qilinmagan


def get_non_zero_streak(user_id):
    """Ketma-ket necha kun zero day bo'lmagan"""
    conn = get_conn()
    today = datetime.now(TZ).date()
    streak = 0
    for i in range(365):
        d = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        found = False
        for table in ["workout_logs", "book_logs", "word_logs", "focus_sessions", "habit_logs", "brain_scores"]:
            row = conn.execute(
                f"SELECT id FROM {table} WHERE user_id=? AND date=? LIMIT 1",
                (user_id, d),
            ).fetchone()
            if row:
                found = True
                break
        if found:
            streak += 1
        else:
            break
    conn.close()
    return streak


# ══════════════════════════════════════════
#  HAFTALIK STATISTIKA
# ══════════════════════════════════════════
def get_weekly_stats(user_id):
    return get_full_stats(user_id, days=7)


# ══════════════════════════════════════════
#  MINI KURSLAR
# ══════════════════════════════════════════
BUILTIN_COURSES = {
    "intizom": {
        "title": "🧱 Intizom kuchi",
        "lessons": [
            {"title": "Intizom nima?", "content": "Intizom — bu motivatsiya yo'q paytda ham to'g'ri ishni qilish qobilyati. U odat orqali shakllanadi."},
            {"title": "Kichik qadamlar", "content": "Katta maqsadlarni kichik kunlik vazifalarga bo'ling. Har kuni 1% yaxshilaning."},
            {"title": "Ertalab rituallar", "content": "Har kuni bir xil vaqtda turing. 5 daqiqa mashq + 10 daqiqa o'qish — shu oddiy boshlanish katta o'zgarish yaratadi."},
            {"title": "Yo'q deyish san'ati", "content": "Keraksiz narsalarga 'yo'q' deyishni o'rganing. Vaqtingiz eng qimmat resursdir."},
            {"title": "30 kunlik qoida", "content": "Yangi odatni 30 kun uzluksiz qiling. Shundan keyin u avtomatik bo'ladi."},
        ],
    },
    "vaqt_boshqaruvi": {
        "title": "⏰ Vaqt boshqaruvi",
        "lessons": [
            {"title": "Pareto qoidasi 80/20", "content": "Natijalarning 80% — ishlarning 20% dan keladi. Eng muhim 20% ni toping va ularga e'tibor bering."},
            {"title": "Pomodoro texnikasi", "content": "25 daqiqa to'liq ishlang, 5 daqiqa dam oling. 4 tadan keyin 15-30 daqiqa uzun tanaffus."},
            {"title": "Time blocking", "content": "Kunni bloklarga bo'ling: ertalab — muhim ishlar, tushdan keyin — uchrashuvlar, kechqurun — o'qish."},
            {"title": "2 daqiqa qoidasi", "content": "Agar ish 2 daqiqadan kam vaqt olsa — hoziroq bajaring. Keyinga qoldirmang."},
            {"title": "Haftalik rejalashtirish", "content": "Har yakshanba kelasi haftani rejalashtiring. 3 ta asosiy maqsad belgilang."},
        ],
    },
    "ingliz_tili": {
        "title": "🇬🇧 Ingliz tili asoslari",
        "lessons": [
            {"title": "Har kuni 5 so'z", "content": "Har kuni 5 ta yangi so'z yod oling va gapda ishlating. Yiliga 1800+ so'z bo'ladi!"},
            {"title": "Shadowing texnikasi", "content": "Ingliz tilidagi audio'ni tinglang va bir vaqtda takrorlang. Bu pronunciation va fluency ni yaxshilaydi."},
            {"title": "Reading habit", "content": "Oddiy inglizcha maqolalar o'qing. Bilmagan so'zlarni yozib oling."},
            {"title": "Thinking in English", "content": "Ichki fikrlaringizni ingliz tilida o'ylashga harakat qiling. Bu eng kuchli mashq."},
            {"title": "1 daqiqalik gapirish", "content": "Har kuni 1 daqiqa o'zingiz bilan inglizcha gaplashing. Timer qo'yib nutq qiling."},
        ],
    },
    "foydali_odatlar": {
        "title": "🌱 Foydali odatlar",
        "lessons": [
            {"title": "Habit stacking", "content": "Yangi odatni eski odatga ulang. Masalan: 'Choy ichgandan keyin 5 daqiqa o'qiyman'."},
            {"title": "Muhit dizayni", "content": "Muhitingizni odat uchun qulay qiling. Kitobni ko'rinadigan joyga qo'ying."},
            {"title": "Streak kuchi", "content": "Ketma-ket kunlarni hisoblang. Streak uzilishidan qo'rqish — kuchli motivator."},
            {"title": "Identity-based habits", "content": "'Men sportchi odamman' deb o'ylang. Shaxsiyatingizni o'zgartiring, odat o'zi keladi."},
            {"title": "1% qoida", "content": "Har kuni 1% yaxshilaning. Yil oxirida 37 baravar yaxshi bo'lasiz (1.01^365 = 37.78)."},
        ],
    },
}


def get_builtin_courses():
    return BUILTIN_COURSES


def add_mini_course_lesson(user_id, course_name, lesson_title):
    conn = get_conn()
    conn.execute(
        "INSERT INTO mini_courses(user_id,course_name,lesson_title,completed_at) VALUES(?,?,?,?)",
        (user_id, course_name, lesson_title, _now()),
    )
    conn.commit()
    conn.close()


def get_course_lessons(user_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT course_name,lesson_title,completed_at FROM mini_courses WHERE user_id=? ORDER BY completed_at DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return [(r["course_name"], r["lesson_title"], r["completed_at"]) for r in rows]


def get_mini_courses(user_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT DISTINCT course_name FROM mini_courses WHERE user_id=?",
        (user_id,),
    ).fetchall()
    conn.close()
    return [r["course_name"] for r in rows]
