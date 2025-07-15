from sqlalchemy.orm import Session
from models.trigger import Trigger
from models.user import User
from schemas.trigger import TriggerBase, TriggerUpdate, CloneRequest


def create_trigger(db: Session, trigger: TriggerBase, user_id: int):
    db_trigger = Trigger(name=trigger.name, user_id=user_id)
    db.add(db_trigger)
    db.commit()
    db.refresh(db_trigger)
    return db_trigger


def get_trigger(db: Session, user_id: int):
    return (
        db.query(Trigger)
        .filter((Trigger.user_id == user_id) | (Trigger.user_id == None))
        .all()
    )


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


def get_default_triggers(db: Session):
    return db.query(Trigger).filter(Trigger.user_id == None).all()


def clone_selected_triggers(data: CloneRequest, db: Session):
    selected = (
        db.query(Trigger)
        .filter(Trigger.id.in_(data.trigger_ids), Trigger.user_id == None)
        .all()
    )
    for t in selected:
        new_trigger = Trigger(name=t.name, user_id=data.user_id)
        db.add(new_trigger)
    db.commit()
    return {"detail": "Déclencheurs copiés"}


def get_user_triggers(db: Session, user: User):
    return db.query(Trigger).filter(Trigger.user_id == user.id).all()
