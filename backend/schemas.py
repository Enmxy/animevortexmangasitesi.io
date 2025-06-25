from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    user: str
    content: str
    manga_id: int
    chapter_id: Optional[int] = None
    rating: int
    ip: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class IPBan(BaseModel):
    id: int
    ip: str
    reason: Optional[str]
    banned_at: datetime
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: int
    class Config:
        orm_mode = True
