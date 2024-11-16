from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Настройка базы данных
DATABASE_URL = "postgresql+asyncpg://kadet:1337228442A@82.146.56.187/naimix_db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()  # Создаем базовый класс для моделей

# Dependency для получения сессии
async def get_db():
    async with async_session() as session:
        yield session
