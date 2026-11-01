from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    #mobile: Optional[str] = Field(None, max_length=15)
    #mobile: Optional[str] = Field(None, max_length=15)
    mobile: str
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    mobile: Optional[str] = None

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str