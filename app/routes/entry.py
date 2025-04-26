from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import entry as crud_entry
from app.schemas.entry import DailyEntryRead, DailyEntryCreate, DailyEntryUpdate
from app.database import SessionLocal

daily_entry_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@daily_entry_router.post("/", response_model=DailyEntryRead)
def create_daily_entry(entry: DailyEntryCreate, db: Session = Depends(get_db)):
    return crud_entry.create_daily_entry(db=db, entry=entry)

@daily_entry_router.get("/", response_model=List[DailyEntryRead])
def read_daily_entries(db: Session = Depends(get_db)):
    return crud_entry.get_daily_entries(db)

@daily_entry_router.get("/{entry_id}", response_model=DailyEntryRead)
def get_daily_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = crud_entry.get_daily_entry_by_id(db, entry_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="DailyEntry non trouvée")
    return db_entry

@daily_entry_router.put("/{entry_id}", response_model=DailyEntryRead)
def update_daily_entry(entry_id: int, entry_update: DailyEntryUpdate, db: Session = Depends(get_db)):
    db_entry = crud_entry.update_daily_entry(db, entry_id, entry_update)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="DailyEntry non trouvée")
    return db_entry

@daily_entry_router.delete("/{entry_id}")
def delete_daily_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = crud_entry.delete_daily_entry(db, entry_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="DailyEntry non trouvée")
    return {"detail": "Daily entry supprimée"}
