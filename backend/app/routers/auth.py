from fastapi import APIRouter, HTTPException, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, LoginRequest
from app.utils.validation import hash_password

from app.utils.auth import verify_password
from app.utils.session import create_session, get_session, delete_session
from app.utils.session import decode_session_token


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


@auth_router.post("/login", summary="Авторизация пользователя")
async def login(credentials: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user_query = await db.execute(select(User).where(User.email == credentials.email))
    user = user_query.scalars().first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Неверные email или пароль")

    # Создаем сессию
    session_data = {"user_id": user.id, "role": user.role, "email": user.email}
    create_session(data=session_data, response=response)
    
    # Возвращаем роль в JSON
    return {"detail": "Авторизация успешна", "role": user.role}


@auth_router.post("/logout", summary="Выход из системы")
async def logout(response: Response):
    """Выход пользователя и удаление сессии."""
    delete_session(response)
    return {"detail": "Вы вышли из системы"}


# Новый маршрут для получения текущей сессии
@auth_router.get("/session", summary="Получить текущую сессию")
async def get_session(request: Request):
    """Возвращает данные текущей сессии пользователя."""
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия не найдена")
    
    session_data = decode_session_token(session_token)
    return {"user_id": session_data["user_id"], "role": session_data["role"]}
