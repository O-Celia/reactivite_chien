from pydantic import BaseModel

class ReactionBase(BaseModel):
    name: str

class ReactionCreate(ReactionBase):
    pass

class ReactionUpdate(ReactionBase):
    pass

class ReactionRead(ReactionBase):
    id: int
    class Config:
        from_attributes = True