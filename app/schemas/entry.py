from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import List, Optional

class DailyEntryBase(BaseModel):
    entry_date: date
    severity: int
    comment: Optional[str] = None

class DailyEntryCreate(DailyEntryBase):
    triggers: List[str]
    reactions: List[str]
    user_id: int

class DailyEntryRead(DailyEntryBase):
    id: int
    user_id: int
    created_at: datetime
    triggers: List[str]
    reactions: List[str]

    class ConfigDict:
        from_attributes = True

class DailyEntryUpdate(BaseModel):
    entry_date: Optional[date] = None
    severity: Optional[int] = None
    comment: Optional[str] = None
    triggers: Optional[List[str]] = None
    reactions: Optional[List[str]] = None

    class ConfigDict:
        from_attributes = True