from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils.validation import hash_password

auth_router = APIRouter(tags=["Authentication"])

@auth_router.post("/register", response_model=UserResponse, summary="Регистрация пользователя")
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверка существующего username
    query_username = await db.execute(select(User).where(User.username == user_data.username))
    if query_username.scalars().first():
        raise HTTPException(status_code=400, detail="Пользователь с таким username уже существует")

    # Проверка существующего email
    query_email = await db.execute(select(User).where(User.email == user_data.email))
    if query_email.scalars().first():
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    # Валидация роли
    if user_data.role not in ["hr", "сотрудник", "кандидат"]:
        raise HTTPException(status_code=400, detail="Недопустимая роль. Выберите hr, сотрудник или кандидат")

    # Хэшируем пароль
    hashed_password = hash_password(user_data.password)

    # Создаем нового пользователя
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
