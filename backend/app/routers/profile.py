from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse

profile_router = APIRouter(tags=["Profile"], prefix="/profile")

@profile_router.get("/{user_id}", response_model=UserResponse, summary="Получить данные пользователя")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@profile_router.put("/{user_id}", summary="Обновить профиль пользователя")
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"detail": "Профиль успешно обновлен"}
