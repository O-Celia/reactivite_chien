from sqlalchemy.orm import Session
from app.models.trigger import Trigger
from app.schemas.trigger import TriggerCreate, TriggerUpdate

def create_trigger(db: Session, trigger: TriggerCreate):
    db_trigger = Trigger(name=trigger.name)
    db.add(db_trigger)
    db.commit()
    db.refresh(db_trigger)
    return db_trigger

def get_trigger(db: Session):
    return db.query(Trigger).all()

def get_trigger_by_id(db: Session, trigger_id: int):
    return db.query(Trigger).filter(Trigger.id == trigger_id).first()

def update_trigger(db: Session, trigger_id: int, updated_data: TriggerUpdate):
    trigger = db.query(Trigger).filter(Trigger.id == trigger_id).first()
    if trigger:
        trigger.name = updated_data.name
        db.commit()
        db.refresh(trigger)
    return trigger

def delete_trigger(db: Session, trigger_id: int):
    trigger = db.query(Trigger).filter(Trigger.id == trigger_id).first()
    if trigger:
        db.delete(trigger)
        db.commit()
    return trigger