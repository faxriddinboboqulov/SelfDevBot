"""⚙️ Bot sozlamalari"""
import os

# 🔑 BotFather dan olingan tokenni shu yerga yozing
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# 🕐 Vaqt zonasi
TIMEZONE = "Asia/Tashkent"

# 🌐 Proxy sozlamasi (Telegram bloklangan bo'lsa)
# Misol: "socks5://127.0.0.1:1080" yoki "http://127.0.0.1:8080"
# Proxy kerak bo'lmasa None qoldiring
PROXY_URL = os.getenv("PROXY_URL", None)

# 🌍 Render.com uchun webhook sozlamasi
# Render avtomatik PORT va RENDER_EXTERNAL_URL beradi
PORT = int(os.getenv("PORT", 8443))
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL", None)
MODE = os.getenv("MODE", "polling")  # "polling" yoki "webhook"
