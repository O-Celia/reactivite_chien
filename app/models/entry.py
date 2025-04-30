from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, Date, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import pytz
from models.trigger import Trigger
from models.reaction import Reaction
from models.user import User

def get_paris_time():
    paris_tz = pytz.timezone("Europe/Paris")
    return datetime.now(paris_tz)

entry_trigger = Table(
    'daily_entry_triggers', Base.metadata,
    Column('entry_id', Integer, ForeignKey('daily_entries.id')),
    Column('trigger_id', Integer, ForeignKey('triggers.id'))
)

entry_reaction = Table(
    'daily_entry_reactions', Base.metadata,
    Column('entry_id', Integer, ForeignKey('daily_entries.id')),
    Column('reaction_id', Integer, ForeignKey('reactions.id'))
)

class DailyEntry(Base):
    __tablename__ = "daily_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    entry_date = Column(Date, nullable = False)
    severity = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_paris_time)

    users = relationship("User")
    triggers = relationship("Trigger", secondary=entry_trigger, backref="entries")
    reactions = relationship("Reaction", secondary=entry_reaction, backref="entries")
