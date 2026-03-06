from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from config import Config

Base = declarative_base()
engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    
    # Pregnancy info
    due_date = Column(DateTime, nullable=True)
    current_week = Column(Integer, default=0)
    is_pregnant = Column(Boolean, default=False)
    
    # Preferences
    language = Column(String(10), default='ru')
    notifications_enabled = Column(Boolean, default=True)
    
    # Stats
    messages_count = Column(Integer, default=0)
    questions_count = Column(Integer, default=0)
    registered_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Health info
    age = Column(Integer, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    pre_pregnancy_weight = Column(Float, nullable=True)
    
    def to_dict(self):
        return {
            'telegram_id': self.telegram_id,
            'username': self.username,
            'first_name': self.first_name,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'current_week': self.current_week,
            'is_pregnant': self.is_pregnant,
            'language': self.language
        }

class ConversationHistory(Base):
    __tablename__ = 'conversation_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    role = Column(String(50))  # 'user' or 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    def get_user_history(cls, session, user_id, limit=50):
        return session.query(cls).filter_by(user_id=user_id)\
            .order_by(cls.timestamp.desc()).limit(limit).all()

class PregnancyTip(Base):
    __tablename__ = 'pregnancy_tips'
    
    id = Column(Integer, primary_key=True)
    week = Column(Integer, nullable=False)
    category = Column(String(100))  # health, nutrition, exercise, etc.
    title = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class MedicalDisclaimer(Base):
    __tablename__ = 'medical_disclaimers'
    
    id = Column(Integer, primary_key=True)
    language = Column(String(10), default='ru')
    content = Column(Text)
    version = Column(String(20))
    updated_at = Column(DateTime, default=datetime.utcnow)

# Создание таблиц
def init_db():
    Base.metadata.create_all(engine)
    
    # Добавляем начальные данные
    session = SessionLocal()
    
    # Добавляем медицинское предупреждение
    disclaimer = session.query(MedicalDisclaimer).filter_by(language='ru').first()
    if not disclaimer:
        disclaimer = MedicalDisclaimer(
            language='ru',
            content="⚠️ *Важное предупреждение*\n\n"
                   "Я - AI-ангел, предоставляющий общую информацию о беременности. "
                   "Я не заменяю профессиональную медицинскую консультацию. "
                   "Всегда консультируйтесь с вашим врачом по вопросам вашего здоровья "
                   "и здоровья вашего будущего ребенка. При возникновении срочных "
                   "медицинских вопросов немедленно обращайтесь к врачу или вызывайте скорую помощь.",
            version="1.0"
        )
        session.add(disclaimer)
        session.commit()
    
    session.close()

# Инициализация базы данных
init_db()