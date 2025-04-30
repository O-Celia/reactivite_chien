from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from routes import user, trigger, reaction, entry
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello and welcome"}

# @router.post("/login")
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if db_user:  # ajouter une vraie vérification de mot de passe
#         return {"message": "Connexion réussie"}
#     raise HTTPException(status_code=401, detail="Échec de la connexion")

app.include_router(user.user_router, prefix="/users", tags=["users"])
app.include_router(trigger.trigger_router, prefix="/triggers", tags=["triggers"])
app.include_router(reaction.reaction_router, prefix="/reactions", tags=["reactions"])
app.include_router(entry.daily_entry_router, prefix="/entry", tags=["entries"])