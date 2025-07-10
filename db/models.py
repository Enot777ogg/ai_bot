from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(128))
    city = Column(String(128))
    last_active = Column(DateTime, default=datetime.utcnow)
    memory = Column(Text)
    
    xp = Column(Integer, default=0)             # опыт
    level = Column(Integer, default=1)          # уровень
    avatar_url = Column(String(512), nullable=True)  # ссылка на аватар
