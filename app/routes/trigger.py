from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import trigger as crud_trigger
from schemas.trigger import TriggerCreate, TriggerRead, TriggerUpdate
from typing import List

trigger_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@trigger_router.post("/", response_model=TriggerRead)
def create_trigger(trigger: TriggerCreate, db: Session = Depends(get_db)):
    return crud_trigger.create_trigger(db=db, trigger=trigger)

@trigger_router.get("/", response_model=List[TriggerRead])
def read_triggers(db: Session = Depends(get_db)):
    return crud_trigger.get_trigger(db)

@trigger_router.get("/{trigger_id}", response_model=TriggerRead)
def get_trigger_by_id(trigger_id: int, db: Session = Depends(get_db)):
    db_trigger = crud_trigger.get_trigger_by_id(db, trigger_id)
    if db_trigger is None:
        raise HTTPException(status_code=404, detail="Déclencheur non trouvé")
    return db_trigger

@trigger_router.put("/{trigger_id}", response_model=TriggerRead)
def update_trigger(trigger_id: int, trigger_update: TriggerUpdate, db: Session = Depends(get_db)):
    db_trigger = crud_trigger.update_trigger(db, trigger_id, trigger_update)
    if db_trigger is None:
        raise HTTPException(status_code=404, detail="Déclencheur non trouvé")
    return db_trigger

@trigger_router.delete("/{trigger_id}", response_model=TriggerRead)
def delete_trigger(trigger_id: int, db: Session = Depends(get_db)):
    db_trigger = crud_trigger.delete_trigger(db, trigger_id)
    if db_trigger is None:
        raise HTTPException(status_code=404, detail="Déclencheur non trouvé")
    return db_trigger
