from fastapi import FastAPI
from app.routers.auth import auth_router
from app.routers.profile import profile_router
from app.routers.role import role_router
from app.database import create_tables
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="User Management Service")

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(role_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить доступ с любых источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить любые HTTP-методы (GET, POST, и т.д.)
    allow_headers=["*"],  # Разрешить любые заголовки
)

@app.on_event("startup")
async def startup():
    await create_tables()

@app.get("/", summary="Тестовый маршрут")
async def root():
    return {"message": "Сервис работает!"}