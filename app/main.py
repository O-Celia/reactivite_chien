from fastapi import FastAPI
import models
from routes import user, trigger, reaction, entry, search
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello and welcome"}

app.include_router(user.user_router, prefix="/users", tags=["users"])
app.include_router(trigger.trigger_router, prefix="/triggers", tags=["triggers"])
app.include_router(reaction.reaction_router, prefix="/reactions", tags=["reactions"])
app.include_router(entry.daily_entry_router, prefix="/entry", tags=["entries"])
app.include_router(search.search_router, prefix="/search", tags=["search"])