from pydantic import BaseModel

class TriggerBase(BaseModel):
    name: str

class TriggerCreate(TriggerBase):
    pass

class TriggerUpdate(TriggerBase):
    pass

class TriggerRead(TriggerBase):
    id: int
    class ConfigDict:
        from_attributes = True