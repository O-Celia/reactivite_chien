from pydantic import BaseModel
from typing import Optional, List

class ReactionBase(BaseModel):
    name: str

class ReactionCreate(ReactionBase):
    user_id: int

class ReactionUpdate(ReactionBase):
    pass

class CloneRequest(BaseModel):
    user_id: int
    reaction_ids: List[int]

class ReactionRead(ReactionBase):
    id: int
    user_id: Optional[int]
    class Config:
        from_attributes = True