# ─────────────────────────────────────────
# config.py  —   Bot sozlamalari
# ─────────────────────────────────────────

# 1. @BotFather dan olingan token
BOT_TOKEN = "8023865690:AAEbAxGdQiJSHbEP4uCsgGYh5qMzHhCge9E"

# 2. Bot egasining Telegram ID-si
#    - Savol yuborilganda SHU ID ga keladi
#    - /lawyer da PAROLSIZ kiradi
#    Topish: @userinfobot ga /start yuboring
OWNER_ID =2080831010       # <── O'ZGARTIRING

# 3. Boshqa yuristlar uchun parol (ixtiyoriy)
LAWYER_PASSWORD = "yuristazizbek"   # <── O'ZGARTIRING

# ─────────────────────────────────────────
# BROADCAST SHABLONLARI
# {video_link} — Instagram havolasi avtomatik joylashadi
# Reklama turida {video_link} bo'sh qoladi
# ─────────────────────────────────────────
TEMPLATES = [
    {
        "name": "📢 Yangilik shablon",
        "text": (
            "📢 <b>Yangi ma'lumot!</b>\n\n"
            "Hurmatli foydalanuvchilar, yuristimiz yangi video tayyorladi!\n\n"
            "🎬 Video: {video_link}\n\n"
            "💬 Savollaringiz bo'lsa, /start orqali yuboring."
        )
    },
    {
        "name": "⚖️ Yuridik maslahat shablon",
        "text": (
            "⚖️ <b>Yuridik maslahat</b>\n\n"
            "Sizga foydali bo'lishi mumkin bo'lgan yangi video:\n\n"
            "🎬 {video_link}\n\n"
            "🤝 <b>Yurist Azizbek</b> — advokatningiz doim yoningizda!"
        )
    },
    {
        "name": "🏛️ Muhim e'lon shablon",
        "text": (
            "🏛️ <b>Muhim e'lon!</b>\n\n"
            "Qonunchilikdagi yangi o'zgarishlar haqida:\n\n"
            "▶️ {video_link}\n\n"
            "📌 E'tiboringiz uchun rahmat!\n"
            "💼 <b>Yurist Azizbek</b> boti"
        )
    },
    # ← Yangi shablon qo'shish:
    # {
    #     "name": "Shablon nomi",
    #     "text": "Matn {video_link} shu yerga"
    # },
]
