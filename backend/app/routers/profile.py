from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse
from app.utils.session import get_session
from datetime import datetime
from app.utils.location import get_coordinates


profile_router = APIRouter(tags=["Profile"], prefix="/profile")

@profile_router.get("/{user_id}", response_model=UserResponse, summary="Получить данные пользователя")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_query = await db.execute(select(User).where(User.id == user_id))
    user = user_query.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Преобразуем coordinates в числа, если они есть
    if user.coordinates:
        try:
            user.coordinates = [float(coord) for coord in user.coordinates]
        except ValueError:
            raise HTTPException(status_code=500, detail="Некорректные координаты в базе данных")

    return user


@profile_router.patch("/{user_id}", summary="Частичное обновление профиля")
async def update_profile(user_id: int, profile_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    user_query = await db.execute(select(User).where(User.id == user_id))
    user = user_query.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Обновляем только переданные поля
    for field, value in profile_data.dict(exclude_unset=True).items():
        if field == "city" and value:
            # Получаем координаты для указанного города
            coordinates = get_coordinates(value)
            user.city = value  # Сохраняем введенный город
            user.coordinates = [coordinates["latitude"], coordinates["longitude"]]  # Сохраняем координаты
        else:
            setattr(user, field, value)  # Обновляем только переданные поля

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"detail": "Профиль успешно обновлен"}




@profile_router.get("/me", summary="Получить данные текущего пользователя")
async def get_current_profile(request: Request):
    """Получение данных текущего пользователя из сессии."""
    session_data = get_session(request)
    return session_data