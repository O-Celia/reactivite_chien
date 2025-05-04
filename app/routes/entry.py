from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from crud import entry as crud_entry
from schemas.entry import DailyEntryRead, DailyEntryCreate, DailyEntryUpdate
from database import SessionLocal
from models.user import User
from utils.dependencies import get_current_user

daily_entry_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@daily_entry_router.post("/", response_model=DailyEntryRead)
def create_daily_entry(
    entry: DailyEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_entry.create_daily_entry(db=db, entry=entry, user_id=current_user.id)

@daily_entry_router.get("/", response_model=List[DailyEntryRead])
def read_user_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_entry.get_daily_entries(db=db, user_id=current_user.id)

@daily_entry_router.get("/{entry_id}", response_model=DailyEntryRead)
def get_entry_by_id(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = crud_entry.get_daily_entry_by_id(db, entry_id)
    if entry is None or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Entrée non trouvée ou non autorisée")
    return entry

@daily_entry_router.put("/{entry_id}", response_model=DailyEntryRead)
def update_entry(
    entry_id: int,
    entry_update: DailyEntryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = crud_entry.get_daily_entry_by_id(db, entry_id)
    if entry is None or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Entrée non trouvée ou non autorisée")
    return crud_entry.update_daily_entry(db, entry_id, entry_update)

@daily_entry_router.delete("/{entry_id}")
def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = crud_entry.get_daily_entry_by_id(db, entry_id)
    if entry is None or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Entrée non trouvée ou non autorisée")
    crud_entry.delete_daily_entry(db, entry_id)
    return {"detail": "Entrée supprimée"}
