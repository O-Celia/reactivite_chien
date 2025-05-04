from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate
from utils.auth import hash_password
from fastapi import HTTPException
from models.trigger import Trigger
from models.reaction import Reaction

def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà utilisé")

    if user.email:
        existing_email = db.query(User).filter(User.email == user.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email déjà utilisé")

    hashed_pw = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password = hashed_pw)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def update_user(db: Session, user_id: int, updated_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        if updated_data.username:
            user.username = updated_data.username
        if updated_data.email:
            user.email = updated_data.email
        if updated_data.password:
            user.hashed_password = hash_password(updated_data.password)
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def update_user_login(user_id: int, update_data: dict, db: Session):
    user = db.query(User).get(user_id)
    if "first_login" in update_data:
        user.first_login = update_data["first_login"]
    db.commit()
    return {"detail": "Utilisateur mis à jour"}
