from fastapi import FastAPI
from app.routers.auth import auth_router
from app.routers.profile import profile_router
from app.routers.role import role_router
from app.database import create_tables

app = FastAPI(title="User Management Service")

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(role_router)


@app.on_event("startup")
async def startup():
    await create_tables()

@app.get("/", summary="Тестовый маршрут")
async def root():
    return {"message": "Сервис работает!"}