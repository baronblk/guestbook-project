from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EntryBase(BaseModel):
    name: str = Field(..., max_length=100)
    stars: int = Field(..., ge=1, le=5)
    comment: str = Field(..., max_length=5000)
    image_url: Optional[str] = None

class EntryCreate(EntryBase):
    pass

class EntryOut(EntryBase):
    id: int
    visible: bool
    created_at: datetime

    class Config:
        orm_mode = True
