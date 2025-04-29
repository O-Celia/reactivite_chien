from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.entry import DailyEntry, Trigger, Reaction, User
from app.schemas.entry import DailyEntryCreate, DailyEntryRead, DailyEntryUpdate

def create_daily_entry(db: Session, entry: DailyEntryCreate):
    
    user = db.query(User).filter(User.id == entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_entry = DailyEntry(
        user_id=entry.user_id,
        entry_date=entry.entry_date,
        severity=entry.severity,
        comment=entry.comment,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    # if entry.triggers:
    #     for trigger_id in entry.triggers:
    #         trigger = db.query(Trigger).filter(Trigger.id == trigger_id).first()
    #         if trigger:
    #             db_entry.triggers.append(trigger)

    # if entry.reactions:
    #     for reaction_id in entry.reactions:
    #         reaction = db.query(Reaction).filter(Reaction.id == reaction_id).first()
    #         if reaction:
    #             db_entry.reactions.append(reaction)

    # db.commit()
    # db.refresh(db_entry)
    
    # Pour les triggers
    if entry.triggers:
        for trigger_name in entry.triggers:
            trigger_name = trigger_name.lower().replace(" ", "_")
            trigger = db.query(Trigger).filter(Trigger.name == trigger_name).first()
            if not trigger:
                trigger = Trigger(name=trigger_name)
                db.add(trigger)
                db.commit()
                db.refresh(trigger)
            db_entry.triggers.append(trigger)

    # Pour les reactions
    if entry.reactions:
        for reaction_name in entry.reactions:
            reaction_name = reaction_name.lower().replace(" ", "_")
            reaction = db.query(Reaction).filter(Reaction.name == reaction_name).first()
            if not reaction:
                reaction = Reaction(name=reaction_name)
                db.add(reaction)
                db.commit()
                db.refresh(reaction)
            db_entry.reactions.append(reaction)
            
    db.commit()
    db.refresh(db_entry)
    
    return DailyEntryRead(
        id=db_entry.id,
        user_id=db_entry.user_id,
        entry_date=db_entry.entry_date,
        severity=db_entry.severity,
        comment=db_entry.comment,
        triggers=[trigger.name for trigger in db_entry.triggers],
        reactions=[reaction.name for reaction in db_entry.reactions],
        created_at=db_entry.created_at
    )

def get_daily_entries(db: Session):
    entries = db.query(DailyEntry).all()
    return [
        DailyEntryRead(
            id=entry.id,
            user_id=entry.user_id,
            entry_date=entry.entry_date,
            severity=entry.severity,
            comment=entry.comment,
            triggers=[trigger.name for trigger in entry.triggers],
            reactions=[reaction.name for reaction in entry.reactions],
            created_at=entry.created_at
        ) for entry in entries
    ]

def get_daily_entry_by_id(db: Session, entry_id: int):
    entry = db.query(DailyEntry).filter(DailyEntry.id == entry_id).first()
    if entry:
        return DailyEntryRead(
            id=entry.id,
            user_id=entry.user_id,
            entry_date=entry.entry_date,
            severity=entry.severity,
            comment=entry.comment,
            triggers=[trigger.name for trigger in entry.triggers],
            reactions=[reaction.name for reaction in entry.reactions],
            created_at=entry.created_at
        )
    return None

def update_daily_entry(db: Session, entry_id: int, entry_update: DailyEntryUpdate):
    db_entry = db.query(DailyEntry).filter(DailyEntry.id == entry_id).first()
    
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # if db_entry:
    if entry_update.entry_date:
        db_entry.entry_date = entry_update.entry_date
    if entry_update.severity is not None:
        db_entry.severity = entry_update.severity
    if entry_update.comment:
        db_entry.comment = entry_update.comment

    if entry_update.triggers is not None:
        db_entry.triggers.clear()
        # for trigger_id in entry_update.triggers:
        #     trigger = db.query(Trigger).filter(Trigger.id == trigger_id).first()
        #     if trigger:
        #         db_entry.triggers.append(trigger)
        for trigger_name in entry_update.triggers:
            trigger_name = trigger_name.strip().lower()
            trigger = db.query(Trigger).filter(Trigger.name == trigger_name).first()
            if not trigger:
                trigger = Trigger(name=trigger_name)
                db.add(trigger)
                db.commit()
                db.refresh(trigger)
            db_entry.triggers.append(trigger)

    if entry_update.reactions is not None:
        db_entry.reactions.clear()
        # for reaction_id in entry_update.reactions:
        #     reaction = db.query(Reaction).filter(Reaction.id == reaction_id).first()
        #     if reaction:
        #         db_entry.reactions.append(reaction)
        for reaction_name in entry_update.reactions:
            reaction_name = reaction_name.strip().lower()
            reaction = db.query(Reaction).filter(Reaction.name == reaction_name).first()
            if not reaction:
                reaction = Reaction(name=reaction_name)
                db.add(reaction)
                db.commit()
                db.refresh(reaction)
            db_entry.reactions.append(reaction)

        db.commit()
        db.refresh(db_entry)
        
    return DailyEntryRead(
        id=db_entry.id,
        user_id=db_entry.user_id,
        entry_date=db_entry.entry_date,
        severity=db_entry.severity,
        comment=db_entry.comment,
        triggers=[trigger.name for trigger in db_entry.triggers],
        reactions=[reaction.name for reaction in db_entry.reactions],
        created_at=db_entry.created_at
    )

def delete_daily_entry(db: Session, entry_id: int):
    db_entry = db.query(DailyEntry).filter(DailyEntry.id == entry_id).first()
    if db_entry:
        db.delete(db_entry)
        db.commit()
        return True
    return None