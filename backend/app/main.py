from fastapi import FastAPI
from app.routers.auth import auth_router
from app.routers.profile import profile_router

app = FastAPI(title="User Management Service")

app.include_router(auth_router)
app.include_router(profile_router)

@app.get("/", summary="Тестовый маршрут")
async def root():
    return {"message": "Сервис работает!"}
