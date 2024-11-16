from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleResponse

role_router = APIRouter(tags=["Roles"], prefix="/roles")

@role_router.get("/", response_model=list[RoleResponse], summary="Получить список ролей")
async def get_roles(db: AsyncSession = Depends(get_db)):
    roles_query = await db.execute(select(Role))
    roles = roles_query.scalars().all()
    return roles

@role_router.post("/", response_model=RoleResponse, summary="Добавить новую роль")
async def create_role(role_data: RoleCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, существует ли роль с таким именем
    role_query = await db.execute(select(Role).where(Role.name == role_data.name))
    existing_role = role_query.scalars().first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Роль с таким именем уже существует")

    # Создаем новую роль
    new_role = Role(name=role_data.name, description=role_data.description)
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)

    return new_role
