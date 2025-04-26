from sqlalchemy.orm import Session
from app.models.reaction import Reaction
from app.schemas.reaction import ReactionCreate, ReactionUpdate

def create_reaction(db: Session, reaction: ReactionCreate):
    db_reaction = Reaction(name=reaction.name)
    db.add(db_reaction)
    db.commit()
    db.refresh(db_reaction)
    return db_reaction

def get_reaction(db: Session):
    return db.query(Reaction).all()

def get_reaction_by_id(db: Session, reaction_id: int):
    return db.query(Reaction).filter(Reaction.id == reaction_id).first()

def update_reaction(db: Session, reaction_id: int, updated_data: ReactionUpdate):
    reaction = db.query(Reaction).filter(Reaction.id == reaction_id).first()
    if reaction:
        reaction.name = updated_data.name
        db.commit()
        db.refresh(reaction)
    return reaction

def delete_reaction(db: Session, reaction_id: int):
    reaction = db.query(Reaction).filter(Reaction.id == reaction_id).first()
    if reaction:
        db.delete(reaction)
        db.commit()
    return reaction