from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base
from datetime import datetime
import pytz
from sqlalchemy.orm import relationship

def get_paris_time():
    paris_tz = pytz.timezone("Europe/Paris")
    return datetime.now(paris_tz)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_paris_time)
    first_login = Column(Boolean, default=True)
    
    triggers = relationship("Trigger", back_populates="user", cascade="all, delete")
    reactions = relationship("Reaction", back_populates="user", cascade="all, delete")
    entries = relationship("DailyEntry", back_populates="user", cascade="all, delete")
