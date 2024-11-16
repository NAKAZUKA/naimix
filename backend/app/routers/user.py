from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserResponse
from app.database import get_db

user_router = APIRouter(prefix="/users", tags=["Users"])

# 1. Получить всех пользователей с ролью "кандидат"
@user_router.get("/candidates", response_model=list[UserResponse], summary="Получить всех кандидатов")
async def get_candidates(db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).where(User.role == "кандидат"))
    candidates = query.scalars().all()
    if not candidates:
        raise HTTPException(status_code=404, detail="Кандидаты не найдены")
    return candidates

# 2. Получить сотрудников компании по ID компании
@user_router.get("/company/{company_id}", response_model=list[UserResponse], summary="Получить сотрудников компании")
async def get_company_employees(company_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).where(User.position == company_id))
    employees = query.scalars().all()
    if not employees:
        raise HTTPException(status_code=404, detail="Сотрудники компании не найдены")
    return employees

# 3. Получить профиль сотрудника компании
@user_router.get("/employee/{user_id}", response_model=UserResponse, summary="Получить профиль сотрудника")
async def get_employee_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).where(User.id == user_id))
    employee = query.scalars().first()
    if not employee:
        raise HTTPException(status_code=404, detail="Профиль сотрудника не найден")
    return employee
