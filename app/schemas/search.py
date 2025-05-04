from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class SearchRequest(BaseModel):
    query: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    triggers: Optional[List[str]] = []
    reactions: Optional[List[str]] = []
    severities: Optional[List[int]] = []

class SearchResult(BaseModel):
    id: int
    entry_date: date
    severity: int
    triggers: List[str]
    reactions: List[str]
    comment: Optional[str]
    
    class ConfigDict:
        from_attributes = True