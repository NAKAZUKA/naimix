from fastapi import FastAPI
from app.routers.auth import auth_router
from app.routers.profile import profile_router
from app.routers.role import role_router
from app.database import create_tables
from fastapi.middleware.cors import CORSMiddleware
from app.routers.team import team_router
from app.routers.user import user_router



app = FastAPI(title="User Management Service")

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(role_router)
app.include_router(team_router)
app.include_router(user_router)

origins = [
    "http://localhost:5174",  # Добавьте ваш фронтенд-URL
    "http://127.0.0.1:5174",  # Добавьте альтернативный адрес
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешаем конкретные источники
    allow_credentials=True,  # Включаем поддержку куки
    allow_methods=["*"],  # Разрешаем любые HTTP-методы
    allow_headers=["*"],  # Разрешаем любые заголовки
)

@app.on_event("startup")
async def startup():
    await create_tables()

@app.get("/", summary="Тестовый маршрут")
async def root():
    return {"message": "Сервис работает!"}