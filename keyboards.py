from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def get_main_keyboard():
    """Основная клавиатура"""
    keyboard = [
        [KeyboardButton("🤰 Моя беременность"), KeyboardButton("📅 Срок беременности")],
        [KeyboardButton("💡 Полезные советы"), KeyboardButton("❓ Задать вопрос")],
        [KeyboardButton("📊 Мой профиль"), KeyboardButton("⚙️ Настройки")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_week_keyboard():
    """Клавиатура для выбора недели"""
    keyboard = []
    row = []
    for week in range(1, 41, 5):
        for w in range(week, min(week+5, 41)):
            row.append(InlineKeyboardButton(str(w), callback_data=f"week_{w}"))
        keyboard.append(row)
        row = []
    return InlineKeyboardMarkup(keyboard)

def get_tip_categories_keyboard():
    """Клавиатура категорий советов"""
    keyboard = [
        [InlineKeyboardButton("🥗 Питание", callback_data="cat_nutrition")],
        [InlineKeyboardButton("🏃‍♀️ Физическая активность", callback_data="cat_exercise")],
        [InlineKeyboardButton("🧘‍♀️ Психологическое здоровье", callback_data="cat_mental")],
        [InlineKeyboardButton("🏥 Медицинские вопросы", callback_data="cat_medical")],
        [InlineKeyboardButton("🛒 Подготовка к родам", callback_data="cat_preparation")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard():
    """Клавиатура настроек"""
    keyboard = [
        [InlineKeyboardButton("🔔 Уведомления", callback_data="settings_notifications")],
        [InlineKeyboardButton("🌐 Язык", callback_data="settings_language")],
        [InlineKeyboardButton("📝 Обновить срок беременности", callback_data="settings_duedate")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_emergency_keyboard():
    """Клавиатура экстренных ситуаций"""
    keyboard = [
        [InlineKeyboardButton("🚑 Вызвать скорую", callback_data="emergency_ambulance")],
        [InlineKeyboardButton("🏥 Ближайший роддом", callback_data="emergency_hospital")],
        [InlineKeyboardButton("📞 Консультация врача", callback_data="emergency_doctor")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)