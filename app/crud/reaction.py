from sqlalchemy.orm import Session
from models.reaction import Reaction
from schemas.reaction import ReactionCreate, ReactionUpdate, CloneRequest

def create_reaction(db: Session, reaction: ReactionCreate):
    db_reaction = Reaction(name=reaction.name, user_id=reaction.user_id)
    db.add(db_reaction)
    db.commit()
    db.refresh(db_reaction)
    return db_reaction

def get_reaction(db: Session, user_id: int):
    return db.query(Reaction).filter((Reaction.user_id == user_id) | (Reaction.user_id == None)).all()

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

def get_default_reactions(db: Session):
    return db.query(Reaction).filter(Reaction.user_id == None).all()

def clone_selected_reactions(data: CloneRequest, db: Session):
    selected = db.query(Reaction).filter(Reaction.id.in_(data.reaction_ids), Reaction.user_id == None).all()
    for r in selected:
        new_reaction = Reaction(name=r.name, user_id=data.user_id)
        db.add(new_reaction)
    db.commit()
    return {"detail": "Réactions copiées"}

def get_user_reactions(db: Session, user_id: int):
    return db.query(Reaction).filter(Reaction.user_id == user_id).all()