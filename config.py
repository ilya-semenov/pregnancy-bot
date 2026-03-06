import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    
    # DeepSeek API
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    DEEPSEEK_MODEL = "deepseek-chat"
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///pregnancy_bot.db')
    
    # Bot settings
    MAX_HISTORY_LENGTH = 50
    MAX_QUESTION_LENGTH = 500
    MAX_MESSAGE_LENGTH = 4000
    
    # Pregnancy trimesters (in weeks)
    FIRST_TRIMESTER = (1, 13)
    SECOND_TRIMESTER = (14, 27)
    THIRD_TRIMESTER = (28, 40)
    
    # Debug
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'