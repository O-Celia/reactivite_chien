from sqlalchemy import Column, Integer, String
from app.database import Base

class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)