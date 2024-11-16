from fastapi import FastAPI
from app.database import create_tables
from app.routers.role import role_router

app = FastAPI(title="Role Management Service")

app.include_router(role_router)

@app.on_event("startup")
async def startup():
    await create_tables()

@app.get("/", summary="Тестовый маршрут")
async def root():
    return {"message": "Сервис работает!"}
