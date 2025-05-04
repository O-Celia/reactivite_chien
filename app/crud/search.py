from sqlalchemy.orm import Session
from models.entry import DailyEntry
from models.trigger import Trigger
from models.reaction import Reaction
from schemas.search import SearchRequest
from typing import List

def search_entries(db: Session, filters: SearchRequest, user_id: int):
    query = db.query(DailyEntry).filter(DailyEntry.user_id == user_id)
    if filters.start_date:
        query = query.filter(DailyEntry.entry_date >= filters.start_date)
    if filters.end_date:
        query = query.filter(DailyEntry.entry_date <= filters.end_date)
    if filters.query:
        query = query.filter(DailyEntry.comment.ilike(f"%{filters.query}%"))
    if filters.severities:
        query = query.filter(DailyEntry.severity.in_(filters.severities))
    if filters.triggers:
        query = query.filter(DailyEntry.triggers.any(Trigger.name.in_(filters.triggers)))
    if filters.reactions:
        query = query.filter(DailyEntry.reactions.any(Reaction.name.in_(filters.reactions)))

    return query.all()
