from pydantic import BaseModel
from typing import Optional, List

class TriggerBase(BaseModel):
    name: str

class TriggerCreate(TriggerBase):
    user_id: int

class TriggerUpdate(TriggerBase):
    pass

class CloneRequest(BaseModel):
    user_id: int
    trigger_ids: List[int]

class TriggerRead(TriggerBase):
    id: int
    user_id: Optional[int]
    class ConfigDict:
        from_attributes = True