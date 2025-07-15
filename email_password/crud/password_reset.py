from sqlalchemy.orm import Session
from models.user import User
from utils.auth import hash_password


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def update_user_password(db: Session, user: User, new_password: str):
    user.password = hash_password(new_password)
    db.commit()
    db.refresh(user)
