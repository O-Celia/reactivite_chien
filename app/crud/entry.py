from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.entry import DailyEntry, Trigger, Reaction, User
from schemas.entry import DailyEntryCreate, DailyEntryRead, DailyEntryUpdate

def create_daily_entry(db: Session, entry: DailyEntryCreate, user_id: int):
    db_entry = DailyEntry(
        user_id=user_id,
        entry_date=entry.entry_date,
        severity=entry.severity,
        comment=entry.comment,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    # Triggers
    if entry.triggers:
        for name in entry.triggers:
            name = name.strip().lower()
            trigger = db.query(Trigger).filter(Trigger.name == name).first()
            if not trigger:
                trigger = Trigger(name=name)
                db.add(trigger)
                db.commit()
                db.refresh(trigger)
            db_entry.triggers.append(trigger)

    # Reactions
    if entry.reactions:
        for name in entry.reactions:
            name = name.strip().lower()
            reaction = db.query(Reaction).filter(Reaction.name == name).first()
            if not reaction:
                reaction = Reaction(name=name)
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
        triggers=[t.name for t in db_entry.triggers],
        reactions=[r.name for r in db_entry.reactions],
        created_at=db_entry.created_at
    )

def get_daily_entries(db: Session, user_id: int):
    entries = db.query(DailyEntry).filter(DailyEntry.user_id == user_id).all()
    return [
        DailyEntryRead(
            id=e.id,
            user_id=e.user_id,
            entry_date=e.entry_date,
            severity=e.severity,
            comment=e.comment,
            triggers=[t.name for t in e.triggers],
            reactions=[r.name for r in e.reactions],
            created_at=e.created_at
        ) for e in entries
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
            triggers=[t.name for t in entry.triggers],
            reactions=[r.name for r in entry.reactions],
            created_at=entry.created_at
        )
    return None

def update_daily_entry(db: Session, entry_id: int, entry_update: DailyEntryUpdate):
    db_entry = db.query(DailyEntry).filter(DailyEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    if entry_update.entry_date:
        db_entry.entry_date = entry_update.entry_date
    if entry_update.severity is not None:
        db_entry.severity = entry_update.severity
    if entry_update.comment:
        db_entry.comment = entry_update.comment

    if entry_update.triggers is not None:
        db_entry.triggers.clear()
        for name in entry_update.triggers:
            name = name.strip().lower()
            trigger = db.query(Trigger).filter(Trigger.name == name).first()
            if not trigger:
                trigger = Trigger(name=name)
                db.add(trigger)
                db.commit()
                db.refresh(trigger)
            db_entry.triggers.append(trigger)

    if entry_update.reactions is not None:
        db_entry.reactions.clear()
        for name in entry_update.reactions:
            name = name.strip().lower()
            reaction = db.query(Reaction).filter(Reaction.name == name).first()
            if not reaction:
                reaction = Reaction(name=name)
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
        triggers=[t.name for t in db_entry.triggers],
        reactions=[r.name for r in db_entry.reactions],
        created_at=db_entry.created_at
    )

def delete_daily_entry(db: Session, entry_id: int):
    db_entry = db.query(DailyEntry).filter(DailyEntry.id == entry_id).first()
    if db_entry:
        db.delete(db_entry)
        db.commit()
        return True
    return None