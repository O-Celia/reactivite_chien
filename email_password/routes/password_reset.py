from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.password_reset import ResetPasswordRequest, ResetPasswordConfirm
from database import SessionLocal
from crud import password_reset
from utils.email import send_reset_email
from utils.auth import create_access_token
from datetime import timedelta
from jose import jwt, JWTError, ExpiredSignatureError
import os

password_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@password_router.post("/request-password-reset")
def request_password_reset(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = password_reset.get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Email introuvable")

    token = create_access_token(
        {"sub": user.username},
        expires_delta=timedelta(
            minutes=int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES", 30))
        ),
    )
    send_reset_email(user.email, token)
    return {"msg": "Email de réinitialisation envoyé."}


@password_router.post("/reset-password")
def reset_password(data: ResetPasswordConfirm, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(data.token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        username = payload.get("sub")
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expiré.")
    except JWTError:
        raise HTTPException(status_code=400, detail="Token invalide.")

    user = password_reset.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    password_reset.update_user_password(db, user, data.new_password)
    return {"msg": "Mot de passe réinitialisé avec succès."}
