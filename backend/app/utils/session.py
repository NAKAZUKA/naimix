import uuid
from fastapi import HTTPException, Request, Response
from typing import Any, Dict
import base64
import json

# Хранилище сессий (в памяти)
sessions: Dict[str, Dict[str, Any]] = {}

def create_session(data: Dict[str, Any], response: Response) -> str:
    """Создает новую сессию и возвращает session_id."""
    session_id = str(uuid.uuid4())  # Уникальный идентификатор сессии
    sessions[session_id] = data  # Сохраняем данные сессии
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return session_id

def get_session(request: Request) -> Dict[str, Any]:
    """Получает данные текущей сессии из cookies."""
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="Сессия недействительна или истекла")
    return sessions[session_id]

def delete_session(response: Response):
    response.delete_cookie("session_token")


def decode_session_token(token: str) -> dict:
    try:
        data = json.loads(base64.urlsafe_b64decode(token).decode())
        if not all(key in data for key in ["user_id", "role", "email"]):
            raise ValueError("Некорректная структура токена")
        return data
    except Exception:
        raise HTTPException(status_code=401, detail="Невалидная сессия")


def create_session(data: dict, response: Response, session_lifetime: int = 3600):
    session_token = base64.urlsafe_b64encode(json.dumps(data).encode()).decode()
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=session_lifetime,
        samesite="Lax",
    )