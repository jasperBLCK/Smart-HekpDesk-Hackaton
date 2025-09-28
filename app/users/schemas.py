from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRead(BaseModel):
    id: str
    username: str
    email: EmailStr
    full_name: str
    phone: str
    role: str
    department: str
    telegram_chat_id: Optional[str] = None
    is_active: bool
    
    
    
class UserCreate(BaseModel):
    id: str
    username: str
    email: EmailStr
    full_name: str
    phone: str
    role: str
    department: str
    telegram_chat_id: Optional[str] = None
    is_active: bool
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    