from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import reaction as crud_reaction
from schemas.reaction import ReactionCreate, ReactionRead, ReactionUpdate, CloneRequest
from typing import List

reaction_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@reaction_router.post("/", response_model=ReactionRead)
def create_reaction(reaction: ReactionCreate, db: Session = Depends(get_db)):
    return crud_reaction.create_reaction(db=db, reaction=reaction)

# @reaction_router.get("/", response_model=List[ReactionRead])
# def read_reactions(user_id: int, db: Session = Depends(get_db)):
#     return crud_reaction.get_reaction(db, user_id)

@reaction_router.get("/default", response_model=List[ReactionRead])
def get_default_reactions(db: Session = Depends(get_db)):
    return crud_reaction.get_default_reactions(db)

@reaction_router.post("/clone_selected")
def clone_selected_reactions(data: CloneRequest, db: Session = Depends(get_db)):
    return crud_reaction.clone_selected_reactions(data, db)

@reaction_router.get("/{reaction_id}", response_model=ReactionRead)
def get_reaction_by_id(reaction_id: int, db: Session = Depends(get_db)):
    db_reaction = crud_reaction.get_reaction_by_id(db, reaction_id)
    if db_reaction is None:
        raise HTTPException(status_code=404, detail="Réaction non trouvée")
    return db_reaction

@reaction_router.put("/{reaction_id}", response_model=ReactionRead)
def update_reaction(reaction_id: int, reaction_update: ReactionUpdate, db: Session = Depends(get_db)):
    db_reaction = crud_reaction.update_reaction(db, reaction_id, reaction_update)
    if db_reaction is None:
        raise HTTPException(status_code=404, detail="Réaction non trouvée")
    return db_reaction

@reaction_router.delete("/{reaction_id}", response_model=ReactionRead)
def delete_reaction(reaction_id: int, db: Session = Depends(get_db)):
    db_reaction = crud_reaction.delete_reaction(db, reaction_id)
    if db_reaction is None:
        raise HTTPException(status_code=404, detail="Réaction non trouvée")
    return db_reaction

@reaction_router.get("/", response_model=List[ReactionRead])
def get_user_reactions(user_id: int, db: Session = Depends(get_db)):
    return crud_reaction.get_user_reactions(db, user_id)