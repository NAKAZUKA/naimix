from pydantic import BaseModel, EmailStr, Field, validator
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
    firstname: Optional[str]
    secondname: Optional[str]
    birthday: Optional[datetime]
    email: str
    role: str
    city: Optional[str]
    bio: Optional[str]
    city: Optional[str]
    coordinates: Optional[List[float]]  # Обязательно указываем тип float

    class Config:
        orm_mode = True


# class UserUpdate(BaseModel):
#     firstname: Optional[str] = None
#     secondname: Optional[str] = None
#     birthday: Optional[datetime] = Field(
#         None,
#         description="Дата рождения в формате: день-месяц-год-час-минута (DD-MM-YYYY HH:MM)"
#     )
#     bio: Optional[str] = None
#     phone_number: Optional[str] = None
#     stack: Optional[str] = None
#     position: Optional[str] = None
#     cosmogram: Optional[str] = None
#     city: Optional[str] = None


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    secondname: Optional[str] = None
    birthday: Optional[str] = Field(
        None,
        description="Дата рождения в формате ISO 8601: YYYY-MM-DDTHH:MM:SS"
    )
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    stack: Optional[str] = None
    position: Optional[str] = None
    city: Optional[str] = None

    @validator("birthday", pre=True, always=True)
    def validate_birthday(cls, value):
        if value:
            try:
                # Проверяем и преобразуем строку в datetime
                datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
                return value
            except ValueError:
                raise ValueError("Некорректный формат даты. Ожидается ISO 8601: YYYY-MM-DDTHH:MM:SS")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str