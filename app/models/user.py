from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime
import pytz

def get_paris_time():
    paris_tz = pytz.timezone("Europe/Paris")
    return datetime.now(paris_tz)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_paris_time)
