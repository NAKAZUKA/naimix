from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Допустимые роли
ALLOWED_ROLES = ["hr", "сотрудник", "кандидат"]

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(..., description="Роль пользователя: hr, сотрудник, кандидат")

    @classmethod
    def validate_role(cls, value: str) -> str:
        if value not in ALLOWED_ROLES:
            raise ValueError(f"Недопустимая роль. Выберите одну из: {', '.join(ALLOWED_ROLES)}")
        return value

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    firstname: Optional[str]
    secondname: Optional[str]
    birthday: Optional[datetime]
    bio: Optional[str]
    coordinates: Optional[List[str]]
    phone_number: Optional[str]
    stack: Optional[str]
    position: Optional[str]
    cosmogram: Optional[str]
