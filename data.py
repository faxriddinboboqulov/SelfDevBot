"""📦 Statik ma'lumotlar — so'zlar, mashqlar, iqtiboslar, videolar, savollar"""
import random


# ══════════════════════════════════════════
#  🌍 INGLIZ TILI SO'ZLARI
# ══════════════════════════════════════════
ENGLISH_WORDS = [
    {"en": "achieve", "uz": "erishmoq"},
    {"en": "believe", "uz": "ishonmoq"},
    {"en": "challenge", "uz": "sinov"},
    {"en": "determine", "uz": "aniqlash"},
    {"en": "effort", "uz": "harakat"},
    {"en": "focus", "uz": "diqqat"},
    {"en": "growth", "uz": "o'sish"},
    {"en": "habit", "uz": "odat"},
    {"en": "improve", "uz": "yaxshilash"},
    {"en": "journey", "uz": "sayohat"},
    {"en": "knowledge", "uz": "bilim"},
    {"en": "learn", "uz": "o'rganmoq"},
    {"en": "mindset", "uz": "fikrlash tarzi"},
    {"en": "never", "uz": "hech qachon"},
    {"en": "opportunity", "uz": "imkoniyat"},
    {"en": "patience", "uz": "sabr"},
    {"en": "quality", "uz": "sifat"},
    {"en": "resilience", "uz": "chidamlilik"},
    {"en": "success", "uz": "muvaffaqiyat"},
    {"en": "transform", "uz": "o'zgartirish"},
    {"en": "unique", "uz": "noyob"},
    {"en": "vision", "uz": "ko'rish/qarash"},
    {"en": "wisdom", "uz": "donolik"},
    {"en": "excellent", "uz": "a'lo"},
    {"en": "year", "uz": "yil"},
    {"en": "goal", "uz": "maqsad"},
    {"en": "strength", "uz": "kuch"},
    {"en": "brave", "uz": "jasur"},
    {"en": "create", "uz": "yaratmoq"},
    {"en": "develop", "uz": "rivojlantirmoq"},
    {"en": "energy", "uz": "energiya"},
    {"en": "freedom", "uz": "erkinlik"},
    {"en": "grateful", "uz": "minnatdor"},
    {"en": "honest", "uz": "halol"},
    {"en": "inspire", "uz": "ilhomlantirmoq"},
    {"en": "justice", "uz": "adolat"},
    {"en": "kind", "uz": "mehribon"},
    {"en": "leader", "uz": "yetakchi"},
    {"en": "motivate", "uz": "rag'batlantirmoq"},
    {"en": "noble", "uz": "olijanob"},
    {"en": "overcome", "uz": "yengmoq"},
    {"en": "purpose", "uz": "maqsad"},
    {"en": "respect", "uz": "hurmat"},
    {"en": "skill", "uz": "ko'nikma"},
    {"en": "trust", "uz": "ishonch"},
    {"en": "understand", "uz": "tushunmoq"},
    {"en": "value", "uz": "qiymat"},
    {"en": "wonder", "uz": "hayrat"},
    {"en": "discipline", "uz": "intizom"},
    {"en": "experience", "uz": "tajriba"},
]


def get_daily_words(count=5):
    return random.sample(ENGLISH_WORDS, min(count, len(ENGLISH_WORDS)))


# ══════════════════════════════════════════
#  💪 MASHQ DASTURLARI
# ══════════════════════════════════════════
WORKOUTS = {
    "Beginner": [
        {"name": "Push-up (tizzadan)", "reps": "3x10", "emoji": "💪"},
        {"name": "Squat", "reps": "3x15", "emoji": "🦵"},
        {"name": "Plank", "reps": "3x20 sek", "emoji": "🧱"},
        {"name": "Jumping Jack", "reps": "3x20", "emoji": "⭐"},
        {"name": "Stretch", "reps": "5 daqiqa", "emoji": "🧘"},
    ],
    "Intermediate": [
        {"name": "Push-up", "reps": "4x15", "emoji": "💪"},
        {"name": "Squat Jump", "reps": "4x12", "emoji": "🦵"},
        {"name": "Plank", "reps": "3x45 sek", "emoji": "🧱"},
        {"name": "Burpee", "reps": "3x10", "emoji": "🔥"},
        {"name": "Mountain Climber", "reps": "3x20", "emoji": "⛰️"},
        {"name": "Lunges", "reps": "3x12 har oyoq", "emoji": "🏃"},
    ],
    "Hard": [
        {"name": "Push-up (keng/tor)", "reps": "5x20", "emoji": "💪"},
        {"name": "Pistol Squat", "reps": "3x8 har oyoq", "emoji": "🦵"},
        {"name": "Plank (dumaloq)", "reps": "3x60 sek", "emoji": "🧱"},
        {"name": "Burpee", "reps": "5x15", "emoji": "🔥"},
        {"name": "Handstand Push-up", "reps": "3x5", "emoji": "🤸"},
        {"name": "Box Jump (stul)", "reps": "4x10", "emoji": "📦"},
        {"name": "Sprint (joyida)", "reps": "5x30 sek", "emoji": "🏃"},
    ],
}


# ══════════════════════════════════════════
#  💡 MOTIVATSION FIKRLAR
# ══════════════════════════════════════════
QUOTES = [
    "💡 «Eng yaxshi vaqt — hozir.» — Konfutsiy",
    "💡 «Intizom — erkinlikdir.» — Jocko Willink",
    "💡 «Har kuni 1% yaxshilaning.» — James Clear",
    "💡 «Katta muvaffaqiyat kichik odatlardan boshlanadi.»",
    "💡 «Sabr — muvaffaqiyatning kaliti.»",
    "💡 «O'qish — aqlning oziq-ovqati.»",
    "💡 «Maqsadsiz hayot — kompas'siz sayohat.»",
    "💡 «Bugun qiyin — ertaga oson bo'ladi.»",
    "💡 «Harakat qilmaslik — eng katta xato.»",
    "💡 «Bilim — kuch.» — Francis Bacon",
    "💡 «Vaqtni tejash — hayotni tejash.»",
    "💡 «Hech kimga taqlid qilmang, o'zingiz bo'ling.»",
    "💡 «Muvaffaqiyat — bu odat.» — Aristotel",
    "💡 «Kelajak bugun boshlagan odamlarga tegishli.»",
    "💡 «1000 millik sayohat bitta qadam bilan boshlanadi.» — Lao Tzu",
    "💡 «Do'stlaringiz — sizning kelajagingiz.»",
    "💡 «Sport — tana uchun, kitob — aql uchun.»",
    "💡 «Har bir professional bir paytlar yangi boshlovchi edi.»",
    "💡 «Qiyinchilik — o'sish belgisi.»",
    "💡 «Ertaga emas, bugun boshlang!»",
    "💡 «Eng yomon reja — rejasizlik.»",
    "💡 «O'zingizga sarflagan vaqt — eng yaxshi investitsiya.»",
    "💡 «Muvaffaqiyat — har kuni kichik ishlarni to'g'ri qilish.»",
    "💡 «Hech qachon o'rganishni to'xtatmang.»",
    "💡 «Kuchli inson — o'zini yenga oladigan inson.»",
    "💡 «Yiqilish — yengilish emas. Turmaslik — yengilish.»",
    "💡 «O'z-o'zini rivojlantirish — eng katta boylik.»",
    "💡 «Har bir kun — yangi imkoniyat.»",
    "💡 «Ish boshlash — eng qiyin qism. Keyin oson.»",
    "💡 «Siz o'zgarishga qodirsiz!»",
]


def get_daily_quote():
    return random.choice(QUOTES)


# ══════════════════════════════════════════
#  🎥 FOYDALI VIDEOLAR
# ══════════════════════════════════════════
VIDEOS = {
    "Motivatsiya": [
        {"title": "Muvaffaqiyat sirlari — TEDx", "url": "https://youtu.be/example1"},
        {"title": "Intizom haqida — Jocko Willink", "url": "https://youtu.be/example2"},
        {"title": "1% qoida — Atomic Habits", "url": "https://youtu.be/example3"},
    ],
    "Sport": [
        {"title": "Uy mashqlari — boshlovchilar", "url": "https://youtu.be/example4"},
        {"title": "15 daqiqalik to'liq trenirovka", "url": "https://youtu.be/example5"},
        {"title": "Stretching — moslashuvchanlik", "url": "https://youtu.be/example6"},
    ],
    "Til o'rganish": [
        {"title": "Ingliz tili — Beginner", "url": "https://youtu.be/example7"},
        {"title": "Pronunciation mashqlari", "url": "https://youtu.be/example8"},
        {"title": "Shadowing technique", "url": "https://youtu.be/example9"},
    ],
    "Biznes": [
        {"title": "Startup asoslari", "url": "https://youtu.be/example10"},
        {"title": "Pul boshqaruvi", "url": "https://youtu.be/example11"},
        {"title": "Marketing strategiya", "url": "https://youtu.be/example12"},
    ],
    "Sog'liq": [
        {"title": "Sog'lom ovqatlanish", "url": "https://youtu.be/example13"},
        {"title": "Uyqu sifatini yaxshilash", "url": "https://youtu.be/example14"},
        {"title": "Stress boshqaruvi", "url": "https://youtu.be/example15"},
    ],
}


def get_videos_by_category(category):
    return VIDEOS.get(category, [])


def get_random_video():
    all_videos = [v for cat in VIDEOS.values() for v in cat]
    return random.choice(all_videos) if all_videos else None


# ══════════════════════════════════════════
#  🧠 MANTIQ SAVOLLARI
# ══════════════════════════════════════════
LOGIC_QUESTIONS = [
    {
        "question": "Agar 5 ta mashina 5 ta qismni 5 daqiqada yasasa, 100 ta mashina 100 ta qismni necha daqiqada yasaydi?",
        "options": ["A) 100 daqiqa", "B) 5 daqiqa", "C) 50 daqiqa", "D) 25 daqiqa"],
        "answer": "B",
    },
    {
        "question": "Ko'lda nilufar gullari har kuni 2 baravar ko'payadi. 48 kunda ko'l to'lsa, yarim ko'l necha kunda to'ladi?",
        "options": ["A) 24 kun", "B) 47 kun", "C) 36 kun", "D) 46 kun"],
        "answer": "B",
    },
    {
        "question": "Bir otaning 5 o'g'li bor. Har bir o'g'ilning 1 ta singlisi bor. Oilada necha bola?",
        "options": ["A) 10", "B) 6", "C) 11", "D) 5"],
        "answer": "B",
    },
    {
        "question": "3 ta sumkada jami 9 ta olma bor. Har bir sumkada toq sondagi olma bor. Bu mumkinmi?",
        "options": ["A) Ha", "B) Yo'q", "C) Ba'zan", "D) Faqat 1 holda"],
        "answer": "A",
    },
    {
        "question": "100 qavatli binoda lift bor. 1-qavatdan 10-qavatga ko'tarilish 1 daqiqa. 1-qavatdan 100-qavatga necha daqiqa?",
        "options": ["A) 10 daqiqa", "B) 11 daqiqa", "C) 9 daqiqa", "D) 100 daqiqa"],
        "answer": "B",
    },
    {
        "question": "5 + 5 + 5 + 5 × 0 = ?",
        "options": ["A) 0", "B) 20", "C) 15", "D) 5"],
        "answer": "C",
    },
    {
        "question": "Soat 3:15 da soat mili bilan daqiqa mili orasidagi burchak necha gradus?",
        "options": ["A) 0°", "B) 7.5°", "C) 15°", "D) 90°"],
        "answer": "B",
    },
    {
        "question": "Bir nechta mushuk bir nechta sichqonni bir necha daqiqada tutadi. 100 ta mushuk 100 ta sichqonni necha daqiqada tutadi?",
        "options": ["A) 1 daqiqa", "B) 100 daqiqa", "C) Bir necha daqiqa", "D) 10 daqiqa"],
        "answer": "C",
    },
    {
        "question": "ABCDEFGH ketma-ketlikda H o'rniga qaysi raqam keladi? A=1, B=2...",
        "options": ["A) 7", "B) 8", "C) 9", "D) 6"],
        "answer": "B",
    },
    {
        "question": "1, 1, 2, 3, 5, 8, 13, ... keyingi son nima?",
        "options": ["A) 18", "B) 20", "C) 21", "D) 26"],
        "answer": "C",
    },
]


def get_random_logic():
    return random.choice(LOGIC_QUESTIONS)


# ══════════════════════════════════════════
#  🔢 TEZKOR MATEMATIKA
# ══════════════════════════════════════════
MATH_QUICK = [
    {"question": "12 × 13 = ?", "options": ["A) 146", "B) 156", "C) 166", "D) 136"], "answer": "B"},
    {"question": "256 ÷ 8 = ?", "options": ["A) 30", "B) 31", "C) 32", "D) 34"], "answer": "C"},
    {"question": "√144 = ?", "options": ["A) 11", "B) 12", "C) 13", "D) 14"], "answer": "B"},
    {"question": "17² = ?", "options": ["A) 279", "B) 289", "C) 299", "D) 269"], "answer": "B"},
    {"question": "1000 - 387 = ?", "options": ["A) 613", "B) 623", "C) 603", "D) 633"], "answer": "A"},
    {"question": "45 × 22 = ?", "options": ["A) 880", "B) 900", "C) 990", "D) 950"], "answer": "C"},
    {"question": "3³ = ?", "options": ["A) 9", "B) 18", "C) 27", "D) 36"], "answer": "C"},
    {"question": "625 ÷ 25 = ?", "options": ["A) 20", "B) 25", "C) 30", "D) 35"], "answer": "B"},
    {"question": "15% × 200 = ?", "options": ["A) 25", "B) 30", "C) 35", "D) 40"], "answer": "B"},
    {"question": "7 × 8 + 6 × 9 = ?", "options": ["A) 100", "B) 110", "C) 120", "D) 130"], "answer": "B"},
    {"question": "√225 = ?", "options": ["A) 13", "B) 14", "C) 15", "D) 16"], "answer": "C"},
    {"question": "888 ÷ 8 = ?", "options": ["A) 101", "B) 111", "C) 121", "D) 108"], "answer": "B"},
    {"question": "25 × 16 = ?", "options": ["A) 380", "B) 390", "C) 400", "D) 410"], "answer": "C"},
    {"question": "2⁸ = ?", "options": ["A) 128", "B) 256", "C) 512", "D) 64"], "answer": "B"},
    {"question": "1001 × 9 = ?", "options": ["A) 9009", "B) 9019", "C) 9099", "D) 9109"], "answer": "A"},
]


def get_random_math():
    return random.choice(MATH_QUICK)


# ══════════════════════════════════════════
#  🏆 CHALLENGE SHABLONLARI
# ══════════════════════════════════════════
CHALLENGE_TEMPLATES = [
    {"title": "💪 7 kun sport", "duration": 7, "desc": "7 kun ketma-ket sport qilish"},
    {"title": "📚 30 kun o'qish", "duration": 30, "desc": "Har kuni kamida 10 sahifa o'qish"},
    {"title": "🌍 14 kun til", "duration": 14, "desc": "Har kuni 5 ta yangi so'z o'rganish"},
    {"title": "🧘 21 kun meditatsiya", "duration": 21, "desc": "Har kuni 10 daqiqa meditatsiya"},
    {"title": "💧 7 kun suv", "duration": 7, "desc": "Har kuni 2 litr suv ichish"},
    {"title": "📵 7 kun detox", "duration": 7, "desc": "Kuniga 1 soatdan ortiq telefon ishlatmaslik"},
    {"title": "✍️ 30 kun jurnal", "duration": 30, "desc": "Har kuni kundalik yozish"},
    {"title": "🏃 21 kun yugurish", "duration": 21, "desc": "Har kuni kamida 15 daqiqa yugurish"},
]


# ══════════════════════════════════════════
#  🛡 ANTI-PROKRASTINATSIYA
# ══════════════════════════════════════════
EASY_TASKS = [
    "📖 1 sahifa kitob o'qi",
    "🏋️ 5 ta push-up qil",
    "🧘 1 daqiqa chuqur nafas ol",
    "📝 1 ta gap yoz (jurnal)",
    "🌍 1 ta yangi so'z o'rgan",
    "💧 1 stakan suv ich",
    "🚶 1 daqiqa yur",
    "🎯 Stol ustini tartibla",
]

PROCRASTINATION_TIPS = [
    "⏰ 5 daqiqa qoidasi: Faqat 5 daqiqa boshlang. Ko'pincha davom etasiz!",
    "🎯 Eng kichik qadamni tanlang: Og'ir ishni bo'laklarga ajrating.",
    "📵 Telefonni boshqa xonaga qo'ying: Distraksiyani yo'q qiling.",
    "🏆 O'zingizga mukofot bering: Ish tugagach, yoqimli narsa qiling.",
    "👥 Kimgadir aytib qo'ying: Javobgarlik hissi motivatsiya beradi.",
    "🔄 2 daqiqa qoidasi: 2 daqiqadan kam ish bo'lsa, hozir qiling!",
    "📋 Faqat 3 ta ish tanlang: Bugun eng muhim 3 vazifaga fokus.",
    "☀️ Eng og'irini birinchi: Ertalab eng qiyin ishni bajaring.",
]
