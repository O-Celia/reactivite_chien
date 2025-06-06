from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import user as crud_user
from schemas.user import UserCreate, UserRead, UserUpdate, TokenResponse, LoginData
from typing import List
from utils.dependencies import get_current_user
from utils.auth import verify_password, create_access_token
from models.user import User

# routes commentées tant qu'il n'y a pas de profil admin

user_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db=db, user=user)


# @user_router.get("/", response_model=List[UserRead])
# def read_users(db: Session = Depends(get_db)):
#     return crud_user.get_users(db)


@user_router.get("/me", response_model=UserRead)
def read_own_profile(current_user: User = Depends(get_current_user)):
    return current_user


# @user_router.get("/username/{username}", response_model=UserRead)
# def get_user_by_username(username: str, db: Session = Depends(get_db)):
#     db_user = crud_user.get_user_by_username(db, username)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
#     return db_user

# @user_router.get("/id/{user_id}", response_model=UserRead)
# def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud_user.get_user_by_id(db, user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
#     return db_user


@user_router.put("/me", response_model=UserRead)
def update_own_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_user.update_user(db, current_user.id, user_update)


# @user_router.put("/id/{user_id}", response_model=UserRead)
# def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
#     db_user = crud_user.update_user(db, user_id, user_update)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
#     return db_user

# @user_router.delete("/id/{user_id}", response_model=UserRead)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud_user.delete_user(db, user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
#     return db_user


@user_router.delete("/me", response_model=UserRead)
def delete_own_account(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return crud_user.delete_user(db, current_user.id)


@user_router.post("/login", response_model=TokenResponse)
def login_json(data: LoginData, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, data.username)
    if (
        not db_user
        or not db_user.hashed_password
        or not verify_password(data.password, db_user.hashed_password)
    ):
        raise HTTPException(
            status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect"
        )
    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}


@user_router.patch("/{user_id}")
def update_user_login(user_id: int, update_data: dict, db: Session = Depends(get_db)):
    return crud_user.update_user_login(user_id, update_data, db)
