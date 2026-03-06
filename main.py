import logging
import aiohttp
import json
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Загружаем настройки
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
DEEPSEEK_KEY = os.getenv('DEEPSEEK_API_KEY')

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Клавиатура (кнопки)
keyboard = [
    [KeyboardButton("🤰 Моя беременность"), KeyboardButton("📅 Срок беременности")],
    [KeyboardButton("💡 Полезные советы"), KeyboardButton("❓ Задать вопрос")],
    [KeyboardButton("🚑 Экстренная помощь")]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Функция для общения с DeepSeek AI
async def ask_deepseek(question):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system", 
                "content": "Ты - опытный консультант по беременности. Отвечай кратко, по делу, на русском языке. Иногда предупреждай, что нужно советоваться с врачом."
            },
            {
                "role": "user", 
                "content": question
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data, timeout=30) as response:
                if response.status == 200:
                    result = await response.json()
                    answer = result['choices'][0]['message']['content']
                    return answer
                else:
                    return "🤖 Извините, я временно не могу ответить. Попробуйте позже."
    except Exception as e:
        print(f"Ошибка: {e}")
        return "🤖 Техническая ошибка. Попробуйте еще раз."

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"Я - AI ангел по беременности. Задай любой вопрос!",
        reply_markup=reply_markup
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    print(f"📨 Сообщение от {user.first_name}: {text}")
    
    # Обработка кнопок
    if text == "🤰 Моя беременность":
        await update.message.reply_text(
            "Расскажите о вашей беременности. Например:\n"
            "• Какая у меня неделя беременности?\n"
            "• Что происходит с ребенком на 20 неделе?\n"
            "• Какие анализы нужно сдать?",
            reply_markup=reply_markup
        )
    
    elif text == "📅 Срок беременности":
        await update.message.reply_text(
            "Чтобы рассчитать точный срок, нужна дата последних месячных или ПДР.\n"
            "Введите дату в формате ДД.ММ.ГГГГ",
            reply_markup=reply_markup
        )
    
    elif text == "💡 Полезные советы":
        await update.message.reply_text(
            "Что вас интересует?\n"
            "• Питание при беременности\n"
            "• Физические упражнения\n"
            "• Подготовка к родам\n"
            "• Развитие ребенка по неделям",
            reply_markup=reply_markup
        )
    
    elif text == "❓ Задать вопрос":
        await update.message.reply_text(
            "Задайте любой вопрос о беременности. Я отвечу с помощью ИИ!",
            reply_markup=reply_markup
        )
    
    elif text == "🚑 Экстренная помощь":
        await update.message.reply_text(
            "🚨 *ЭКСТРЕННАЯ ПОМОЩЬ*\n\n"
            "Если у вас:\n"
            "• Кровотечение\n"
            "• Сильные боли\n"
            "• Высокая температура\n"
            "• Отсутствие шевелений\n\n"
            "НЕМЕДЛЕННО звоните: **103** или **112**",
            parse_mode='Markdown'
        )
    
    else:
        # ВКЛЮЧАЕМ ИНДИКАТОР ПЕЧАТИ (бот "печатает")
        async def send_action():
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Запускаем индикатор печати каждые 3 секунды
        stop_printing = False
        async def keep_typing():
            while not stop_printing:
                await send_action()
                await asyncio.sleep(3)
        
        # Запускаем фоновую задачу
        typing_task = asyncio.create_task(keep_typing())
        
        try:
            # Получаем ответ от ИИ
            answer = await ask_deepseek(text)
            
            # Останавливаем индикатор печати
            stop_printing = True
            typing_task.cancel()
            
            # Добавляем предупреждение
            full_answer = f"{answer}\n\n---\n⚠️ *Важно*: Я - ИИ-ангел. Всегда консультируйтесь с врачом!"
            
            await update.message.reply_text(
                full_answer,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            
        except Exception as e:
            # Останавливаем индикатор в случае ошибки
            stop_printing = True
            typing_task.cancel()
            
            await update.message.reply_text(
                "❌ Произошла ошибка. Попробуйте еще раз.",
                reply_markup=reply_markup
            )

# Команда для теста
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает! DeepSeek подключен.")

print("=" * 60)
print("🤖 AI БОТ ДЛЯ БЕРЕМЕННЫХ ЗАПУЩЕН")
print("=" * 60)
print(f"📱 Имя бота: @girls_pregnancy_bot")
print(f"🔑 DeepSeek: {'✅ Подключен' if DEEPSEEK_KEY else '❌ НЕТ КЛЮЧА'}")
print("✨ Теперь бот показывает 'печатает...' когда думает")
print("=" * 60)

# Запуск бота
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("test", test))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()