import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler, CallbackQueryHandler
)
from config import BOT_TOKEN, LAWYER_PASSWORD, OWNER_ID, TEMPLATES
from database import Database

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

db = Database()

# ─── STATES ───
(
    LANG_SELECT, MAIN_MENU,
    LEGAL_HELP_MENU, DOC_CREATE_MENU,
    CALCULATORS_MENU, DOC_CHECK_MENU, LAWYER_SERVICE_MENU,
    QUESTION_TEXT,
    LAWYER_PASSWORD_STATE, LAWYER_PANEL,
    LAWYER_VIDEO_LINK, LAWYER_VIDEO_TEMPLATE,
    LAWYER_SIMPLE_MSG,
    LAWYER_AD_TEXT, LAWYER_AD_TEMPLATE,
) = range(15)

# ─── TEXTS ───
TEXTS = {
    "uz": {
        "welcome": "👋 Assalomu alaykum!\n\n<b>Yurist Azizbek</b> — yuridik savollaringizga tez va aniq javob beruvchi botga xush kelibsiz! Advokatningiz doim yoningizda 🤝\n\nQuyidagi menyudan kerakli bo'limni tanlang 👇",
        "choose_lang": "🌐 Tilni tanlang / Выберите язык:",
        "main_menu": "📋 Asosiy menyu:",
        "back": "🔙 Ortga",
        "legal_help": "📚 Yuridik yordam",
        "doc_create": "📄 Hujjat yaratish",
        "question_send": "💬 Savol yuborish",
        "calculators": "🧮 Yuridik kalkulyatorlar",
        "doc_check": "🔍 Hujjat tekshirish",
        "lawyer_service": "👨‍💼 Advokat xizmati",
        "legal_help_menu": "📚 Yuridik yordam bo'limlari:",
        "doc_create_menu": "📄 Hujjat yaratish bo'limlari:",
        "calculators_menu": "🧮 Kalkulyatorlar bo'limlari:",
        "doc_check_menu": "🔍 Hujjat tekshirish bo'limlari:",
        "lawyer_service_menu": "👨‍💼 Advokat xizmati bo'limlari:",
        "send_question": "✏️ Savolingizni yozing, yurist tez orada javob beradi:",
        "question_sent": "✅ Savolingiz yuristga yuborildi! Tez orada javob olasiz.",
        "section_soon": "🚧 Bu bo'lim tez orada ishga tushadi. Kuting!",
        "lh1": "⚖️ Fuqarolik huquqi", "lh2": "🏠 Mulk va turar-joy",
        "lh3": "👨‍👩‍👧 Oila va nikoh huquqi", "lh4": "💼 Mehnat huquqi",
        "lh5": "🏢 Tadbirkorlik huquqi", "lh6": "🚔 Jinoyat huquqi",
        "dc1": "📝 Ariza yozish", "dc2": "📃 Shartnoma tuzish",
        "dc3": "🗂️ Da'vo arizasi", "dc4": "📋 Ishonchnoma",
        "dc5": "🔖 Vasiyatnoma", "dc6": "📑 Boshqa hujjatlar",
        "cal1": "💰 Nafaqa kalkulyatori", "cal2": "⚖️ Da'vo summasi",
        "cal3": "🏦 Jarima kalkulyatori", "cal4": "📅 Muddat hisoblagich",
        "cal5": "💵 Davlat boji", "cal6": "📊 Kompensatsiya",
        "dch1": "📄 Shartnoma tekshirish", "dch2": "🔎 Ariza tekshirish",
        "dch3": "📑 Vasiyatnoma tekshirish", "dch4": "📋 Ishonchnoma tekshirish",
        "dch5": "🗂️ Boshqa hujjat", "dch6": "💡 Maslahat olish",
        "ls1": "📞 Konsultatsiya", "ls2": "🏛️ Sudda vakillik",
        "ls3": "📝 Hujjat tayyorlash", "ls4": "🤝 Muzokaralar",
        "ls5": "🔍 Huquqiy ekspertiza", "ls6": "💼 Biznes huquqi",
        "enter_password": "🔐 Yurist paneli uchun parolni kiriting:",
        "wrong_password": "❌ Noto'g'ri parol! Qayta urinib ko'ring.",
        "lawyer_welcome": "✅ Xush kelibsiz, yurist!\n\n👇 Broadcast turini tanlang:",
        "btn_video": "🎬 Video havolasi",
        "btn_simple": "📝 Oddiy xabar",
        "btn_ad": "📣 Reklama",
        "lawyer_stats": "📊 Statistika",
        "lawyer_exit": "🚪 Chiqish",
        "send_video_link": "🎬 Instagram video havolasini yuboring:",
        "select_template": "📋 Shablonni tanlang:",
        "invalid_link": "❌ Noto'g'ri havola! Instagram havolasini yuboring.",
        "send_simple_msg": "📝 Hammaga yuboriladigan xabarni yozing:",
        "send_ad_text": "📣 Reklama matnini yozing:",
        "select_ad_tpl": "📋 Reklama shablonini tanlang:",
        "broadcast_sent": "✅ {} ta foydalanuvchiga yuborildi!",
        "stats_text": "📊 Bot statistikasi:\n👥 Jami foydalanuvchilar: {}\n📨 Yuborilgan savollar: {}",
    },
    "ru": {
        "welcome": "👋 Ассалому алайкум!\n\n<b>Yurist Azizbek</b> — добро пожаловать в бот для быстрых и точных ответов на юридические вопросы! Ваш адвокат всегда рядом 🤝\n\nВыберите нужный раздел из меню ниже 👇",
        "choose_lang": "🌐 Tilni tanlang / Выберите язык:",
        "main_menu": "📋 Главное меню:",
        "back": "🔙 Назад",
        "legal_help": "📚 Юридическая помощь",
        "doc_create": "📄 Создание документов",
        "question_send": "💬 Задать вопрос",
        "calculators": "🧮 Юридические калькуляторы",
        "doc_check": "🔍 Проверка документов",
        "lawyer_service": "👨‍💼 Услуги адвоката",
        "legal_help_menu": "📚 Разделы юридической помощи:",
        "doc_create_menu": "📄 Разделы создания документов:",
        "calculators_menu": "🧮 Разделы калькуляторов:",
        "doc_check_menu": "🔍 Разделы проверки документов:",
        "lawyer_service_menu": "👨‍💼 Разделы услуг адвоката:",
        "send_question": "✏️ Напишите ваш вопрос, юрист скоро ответит:",
        "question_sent": "✅ Ваш вопрос отправлен юристу! Скоро получите ответ.",
        "section_soon": "🚧 Этот раздел скоро заработает. Ждите!",
        "lh1": "⚖️ Гражданское право", "lh2": "🏠 Имущество и жильё",
        "lh3": "👨‍👩‍👧 Семейное право", "lh4": "💼 Трудовое право",
        "lh5": "🏢 Предпринимательство", "lh6": "🚔 Уголовное право",
        "dc1": "📝 Написать заявление", "dc2": "📃 Составить договор",
        "dc3": "🗂️ Исковое заявление", "dc4": "📋 Доверенность",
        "dc5": "🔖 Завещание", "dc6": "📑 Другие документы",
        "cal1": "💰 Калькулятор алим.", "cal2": "⚖️ Сумма иска",
        "cal3": "🏦 Калькулятор штраф.", "cal4": "📅 Счётчик сроков",
        "cal5": "💵 Госпошлина", "cal6": "📊 Компенсация",
        "dch1": "📄 Проверка договора", "dch2": "🔎 Проверка заявления",
        "dch3": "📑 Проверка завещания", "dch4": "📋 Проверка доверенн.",
        "dch5": "🗂️ Другой документ", "dch6": "💡 Получить совет",
        "ls1": "📞 Консультация", "ls2": "🏛️ Представительство",
        "ls3": "📝 Подготовка документ.", "ls4": "🤝 Переговоры",
        "ls5": "🔍 Правовая экспертиза", "ls6": "💼 Бизнес-право",
        "enter_password": "🔐 Введите пароль для панели юриста:",
        "wrong_password": "❌ Неверный пароль! Попробуйте снова.",
        "lawyer_welcome": "✅ Добро пожаловать, юрист!\n\n👇 Выберите тип broadcast:",
        "btn_video": "🎬 Ссылка на видео",
        "btn_simple": "📝 Обычное сообщение",
        "btn_ad": "📣 Реклама",
        "lawyer_stats": "📊 Статистика",
        "lawyer_exit": "🚪 Выйти",
        "send_video_link": "🎬 Отправьте ссылку на Instagram видео:",
        "select_template": "📋 Выберите шаблон:",
        "invalid_link": "❌ Неверная ссылка! Отправьте ссылку Instagram.",
        "send_simple_msg": "📝 Напишите сообщение для всех пользователей:",
        "send_ad_text": "📣 Напишите текст рекламы:",
        "select_ad_tpl": "📋 Выберите шаблон рекламы:",
        "broadcast_sent": "✅ Отправлено {} пользователям!",
        "stats_text": "📊 Статистика бота:\n👥 Всего пользователей: {}\n📨 Отправлено вопросов: {}",
    }
}

def t(uid, key):
    lang = db.get_user_lang(uid) or "uz"
    return TEXTS[lang].get(key, key)

# ─── KEYBOARDS ───
def lang_keyboard():
    return ReplyKeyboardMarkup([["🇺🇿 O'zbekcha", "🇷🇺 Русский",]], resize_keyboard=True, one_time_keyboard=True)

def main_menu_keyboard(uid):
    return ReplyKeyboardMarkup([
        [t(uid,"legal_help"), t(uid,"doc_create")],
        [t(uid,"question_send")],
        [t(uid,"calculators"), t(uid,"doc_check")],
        [t(uid,"lawyer_service")],
    ], resize_keyboard=True)

def back_keyboard(uid):
    return ReplyKeyboardMarkup([[t(uid,"back")]], resize_keyboard=True)

def sub_keyboard(uid, keys):
    rows = [keys[i:i+2] for i in range(0, len(keys), 2)]
    rows.append(["back"])
    return ReplyKeyboardMarkup([[t(uid,k) for k in row] for row in rows], resize_keyboard=True)

def lawyer_panel_keyboard(uid):
    return ReplyKeyboardMarkup([
        [t(uid,"btn_video")],
        [t(uid,"btn_simple")],
        [t(uid,"btn_ad")],
        [t(uid,"lawyer_stats"), t(uid,"lawyer_exit")],
    ], resize_keyboard=True)

def templates_inline(prefix="tpl"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(tpl["name"], callback_data=f"{prefix}_{i}")]
        for i, tpl in enumerate(TEMPLATES)
    ])

def cancel_keyboard():
    return ReplyKeyboardMarkup([["❌ Bekor qilish"]], resize_keyboard=True)

# ─── HELPERS ───
def is_back(uid, text):
    return text in ["🔙 Ortga", "🔙 Назад", t(uid,"back")]

def is_instagram(url):
    return "instagram.com" in url or "instagr.am" in url

async def broadcast(context, text, parse_mode="HTML"):
    sent = 0
    for uid in db.get_all_users():
        try:
            await context.bot.send_message(chat_id=uid, text=text, parse_mode=parse_mode)
            sent += 1
        except Exception:
            pass
    return sent

# ─── USER HANDLERS ───
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username or "", user.full_name or "")
    await update.message.reply_text(TEXTS["uz"]["choose_lang"], reply_markup=lang_keyboard())
    return LANG_SELECT

async def lang_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = "ru" if "Русский" in update.message.text else "uz"
    db.set_user_lang(uid, lang)
    await update.message.reply_text(t(uid,"welcome"), parse_mode="HTML", reply_markup=main_menu_keyboard(uid))
    return MAIN_MENU

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    if text == t(uid,"legal_help"):
        await update.message.reply_text(t(uid,"legal_help_menu"), reply_markup=sub_keyboard(uid,["lh1","lh2","lh3","lh4","lh5","lh6"]))
        return LEGAL_HELP_MENU
    if text == t(uid,"doc_create"):
        await update.message.reply_text(t(uid,"doc_create_menu"), reply_markup=sub_keyboard(uid,["dc1","dc2","dc3","dc4","dc5","dc6"]))
        return DOC_CREATE_MENU
    if text == t(uid,"question_send"):
        await update.message.reply_text(t(uid,"send_question"), reply_markup=back_keyboard(uid))
        return QUESTION_TEXT
    if text == t(uid,"calculators"):
        await update.message.reply_text(t(uid,"calculators_menu"), reply_markup=sub_keyboard(uid,["cal1","cal2","cal3","cal4","cal5","cal6"]))
        return CALCULATORS_MENU
    if text == t(uid,"doc_check"):
        await update.message.reply_text(t(uid,"doc_check_menu"), reply_markup=sub_keyboard(uid,["dch1","dch2","dch3","dch4","dch5","dch6"]))
        return DOC_CHECK_MENU
    if text == t(uid,"lawyer_service"):
        await update.message.reply_text(t(uid,"lawyer_service_menu"), reply_markup=sub_keyboard(uid,["ls1","ls2","ls3","ls4","ls5","ls6"]))
        return LAWYER_SERVICE_MENU
    return MAIN_MENU

async def _sub(update, context, state):
    uid = update.effective_user.id
    if is_back(uid, update.message.text):
        await update.message.reply_text(t(uid,"main_menu"), reply_markup=main_menu_keyboard(uid))
        return MAIN_MENU
    await update.message.reply_text(t(uid,"section_soon"))
    return state

async def legal_help_handler(u, c):    return await _sub(u, c, LEGAL_HELP_MENU)
async def doc_create_handler(u, c):    return await _sub(u, c, DOC_CREATE_MENU)
async def calculators_handler(u, c):   return await _sub(u, c, CALCULATORS_MENU)
async def doc_check_handler(u, c):     return await _sub(u, c, DOC_CHECK_MENU)
async def lawyer_service_handler(u, c):return await _sub(u, c, LAWYER_SERVICE_MENU)

async def question_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = update.effective_user
    text = update.message.text
    if is_back(uid, text):
        await update.message.reply_text(t(uid,"main_menu"), reply_markup=main_menu_keyboard(uid))
        return MAIN_MENU
    try:
        uname = user.username or "noma'lum"
        msg_text = f"📨 <b>Yangi savol!</b>\n\n👤 {user.full_name} (@{uname})\n🆔 <code>{uid}</code>\n\n❓ {text}"
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=msg_text,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Yuristga xato: {e}")
    db.increment_questions()
    await update.message.reply_text(t(uid,"question_sent"), reply_markup=main_menu_keyboard(uid))
    return MAIN_MENU

# ─── LAWYER PANEL ───
async def lawyer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    db.add_user(uid, update.effective_user.username or "", update.effective_user.full_name or "")
    # Bot egasi — parolsiz kiradi
    if uid == OWNER_ID:
        await update.message.reply_text(t(uid,"lawyer_welcome"), reply_markup=lawyer_panel_keyboard(uid))
        return LAWYER_PANEL
    # Boshqalar — parol
    await update.message.reply_text(t(uid,"enter_password"), reply_markup=cancel_keyboard())
    return LAWYER_PASSWORD_STATE

async def lawyer_password_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    if text == "❌ Bekor qilish":
        await update.message.reply_text(t(uid,"main_menu"), reply_markup=main_menu_keyboard(uid))
        return MAIN_MENU
    if text == LAWYER_PASSWORD:
        await update.message.reply_text(t(uid,"lawyer_welcome"), reply_markup=lawyer_panel_keyboard(uid))
        return LAWYER_PANEL
    await update.message.reply_text(t(uid,"wrong_password"))
    return LAWYER_PASSWORD_STATE

async def lawyer_panel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    if text == t(uid,"btn_video"):
        await update.message.reply_text(t(uid,"send_video_link"), reply_markup=back_keyboard(uid))
        return LAWYER_VIDEO_LINK
    if text == t(uid,"btn_simple"):
        await update.message.reply_text(t(uid,"send_simple_msg"), reply_markup=back_keyboard(uid))
        return LAWYER_SIMPLE_MSG
    if text == t(uid,"btn_ad"):
        await update.message.reply_text(t(uid,"send_ad_text"), reply_markup=back_keyboard(uid))
        return LAWYER_AD_TEXT
    if text == t(uid,"lawyer_stats"):
        await update.message.reply_text(t(uid,"stats_text").format(db.get_users_count(), db.get_questions_count()))
        return LAWYER_PANEL
    if text == t(uid,"lawyer_exit"):
        await update.message.reply_text(t(uid,"main_menu"), reply_markup=main_menu_keyboard(uid))
        return MAIN_MENU
    return LAWYER_PANEL

# ── 1. Video ──
async def lawyer_video_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    if is_back(uid, text):
        await update.message.reply_text(t(uid,"lawyer_welcome"), reply_markup=lawyer_panel_keyboard(uid))
        return LAWYER_PANEL
    if not is_instagram(text):
        await update.message.reply_text(t(uid,"invalid_link"))
        return LAWYER_VIDEO_LINK
    context.user_data["video_link"] = text
    await update.message.reply_text(t(uid,"select_template"), reply_markup=templates_inline("tpl"))
    return LAWYER_VIDEO_TEMPLATE

async def video_template_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()
    idx = int(query.data.split("_")[1])
    link = context.user_data.get("video_link", "")
    msg = TEMPLATES[idx]["text"].format(video_link=link)
    sent = await broadcast(context, msg)
    await query.edit_message_text(t(uid,"broadcast_sent").format(sent))
    await context.bot.send_message(chat_id=uid, text=t(uid,"lawyer_welcome"), reply_markup=lawyer_panel_keyboard(uid))
    return LAWYER_PANEL

# ── 2. Oddiy xabar ──
async def lawyer_simple_msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    if is_back(uid, text):
        await update.message.reply_text(t(uid,"lawyer_welcome"), reply_markup=lawyer_panel_keyboard(uid))
        return LAWYER_PANEL
    sent = await broadcast(context, text, parse_mode=None)
    await update.message.reply_text(t(uid,"broadcast_sent").format(sent), reply_markup=lawyer_panel_keyboard(uid))
    return LAWYER_PANEL

# ── 3. Reklama ──
async def lawyer_ad_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    if is_back(uid, text):
        await update.message.reply_text(t(uid,"lawyer_welcome"), reply_markup=lawyer_panel_keyboard(uid))
        return LAWYER_PANEL
    context.user_data["ad_text"] = text
    await update.message.reply_text(t(uid,"select_ad_tpl"), reply_markup=templates_inline("adtpl"))
    return LAWYER_AD_TEMPLATE

async def ad_template_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()
    idx = int(query.data.split("_")[1])
    ad_text = context.user_data.get("ad_text", "")
    base = TEMPLATES[idx]["text"].format(video_link="").strip()
    msg = f"{base}\n\n📣 <b>Reklama:</b>\n{ad_text}"
    sent = await broadcast(context, msg)
    await query.edit_message_text(t(uid,"broadcast_sent").format(sent))
    await context.bot.send_message(chat_id=uid, text=t(uid,"lawyer_welcome"), reply_markup=lawyer_panel_keyboard(uid))
    return LAWYER_PANEL

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(t(uid,"main_menu"), reply_markup=main_menu_keyboard(uid))
    return MAIN_MENU

# ─── MAIN ───
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("lawyer", lawyer_command)],
        states={
            LANG_SELECT:           [MessageHandler(filters.TEXT & ~filters.COMMAND, lang_select)],
            MAIN_MENU:             [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)],
            LEGAL_HELP_MENU:       [MessageHandler(filters.TEXT & ~filters.COMMAND, legal_help_handler)],
            DOC_CREATE_MENU:       [MessageHandler(filters.TEXT & ~filters.COMMAND, doc_create_handler)],
            CALCULATORS_MENU:      [MessageHandler(filters.TEXT & ~filters.COMMAND, calculators_handler)],
            DOC_CHECK_MENU:        [MessageHandler(filters.TEXT & ~filters.COMMAND, doc_check_handler)],
            LAWYER_SERVICE_MENU:   [MessageHandler(filters.TEXT & ~filters.COMMAND, lawyer_service_handler)],
            QUESTION_TEXT:         [MessageHandler(filters.TEXT & ~filters.COMMAND, question_text_handler)],
            LAWYER_PASSWORD_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, lawyer_password_handler)],
            LAWYER_PANEL:          [MessageHandler(filters.TEXT & ~filters.COMMAND, lawyer_panel_handler)],
            LAWYER_VIDEO_LINK:     [MessageHandler(filters.TEXT & ~filters.COMMAND, lawyer_video_link_handler)],
            LAWYER_VIDEO_TEMPLATE: [CallbackQueryHandler(video_template_callback, pattern=r"^tpl_\d+$")],
            LAWYER_SIMPLE_MSG:     [MessageHandler(filters.TEXT & ~filters.COMMAND, lawyer_simple_msg_handler)],
            LAWYER_AD_TEXT:        [MessageHandler(filters.TEXT & ~filters.COMMAND, lawyer_ad_text_handler)],
            LAWYER_AD_TEMPLATE:    [CallbackQueryHandler(ad_template_callback, pattern=r"^adtpl_\d+$")],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start),
            CommandHandler("lawyer", lawyer_command),
        ],
        allow_reentry=True,
    )
    app.add_handler(conv)
    logger.info("✅ Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()

