from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import trigger as crud_trigger
from schemas.trigger import TriggerCreate, TriggerRead, TriggerUpdate, CloneRequest
from typing import List
from utils.dependencies import get_current_user
from models.user import User

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

# @trigger_router.get("/", response_model=List[TriggerRead])
# def get_user_triggers(user_id: int, db: Session = Depends(get_db)):
#     return crud_trigger.get_user_triggers(db, user_id)

@trigger_router.get("/", response_model=List[TriggerRead])
def get_user_triggers(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_trigger.get_user_triggers(db, current_user)

@trigger_router.get("/default", response_model=List[TriggerRead])
def get_default_triggers(db: Session = Depends(get_db)):
    return crud_trigger.get_default_triggers(db)

@trigger_router.post("/clone_selected")
def clone_selected_triggers(data: CloneRequest, db: Session = Depends(get_db)):
    return crud_trigger.clone_selected_triggers(data, db)

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
