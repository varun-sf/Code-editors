from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSignup(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str 
    password: str

class CodeFileBase(BaseModel):
    filename: str

class CodeFileCreate(CodeFileBase):
    content: str

class CodeFileUpdate(BaseModel):
    content: Optional[str] = None

class CodeFileResponse(CodeFileBase):
    id: int
    content: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
