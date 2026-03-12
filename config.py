"""⚙️ Bot sozlamalari"""
import os

# 🔑 BotFather dan olingan tokenni shu yerga yozing
# Render.com da environment variable sifatida qo'ying
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# 🕐 Vaqt zonasi
TIMEZONE = "Asia/Tashkent"

# 🌐 Proxy sozlamasi (Telegram bloklangan bo'lsa)
PROXY_URL = os.getenv("PROXY_URL", None)

# 🌐 Render.com uchun webhook sozlamasi
PORT = int(os.getenv("PORT", 8443))
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL", None)
MODE = os.getenv("MODE", "polling")  # "polling" yoki "webhook"
