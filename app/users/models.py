from sqlalchemy import Column, String, Boolean
from app.database import Base  # ← Абсолютный импорт из app.database




class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(String, nullable=False)
    department = Column(String, nullable=True)
    telegram_chat_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

        
    
"""    User (Пользователь)
{
  "id": "user_123",
  "username": "v.ivanov",
  "email": "v.ivanov@academy.ru",
  "full_name": "Владимир Иванов",
  "phone": "+7-XXX-XXX-XXXX",
  "role": "employee",
  "department": "Кафедра математики",
  "telegram_chat_id": "123456789",
  "is_active": true,
  "notification_settings": {
    "telegram": true,
    "email": false,
    "working_hours": "09:00-18:00"
  }
}"""