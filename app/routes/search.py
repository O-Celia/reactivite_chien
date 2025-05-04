from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.search import SearchRequest, SearchResult
from crud.search import search_entries
from typing import List
from database import SessionLocal
from models.user import User
from utils.dependencies import get_current_user

search_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@search_router.post("/", response_model=List[SearchResult])
def search(payload: SearchRequest, 
           db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)):
    results = search_entries(db, payload, user_id=current_user.id)
    return [
        SearchResult(
            id=entry.id,
            entry_date=entry.entry_date,
            severity=entry.severity,
            triggers=[t.name for t in entry.triggers],
            reactions=[r.name for r in entry.reactions],
            comment=entry.comment
        )
        for entry in results
    ]
