import uuid
from fastapi import HTTPException, Request, Response
from typing import Any, Dict
import base64
import json

# Хранилище сессий (в памяти)
sessions: Dict[str, Dict[str, Any]] = {}


def get_session(request: Request) -> Dict[str, Any]:
    """Получает данные текущей сессии из cookies."""
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="Сессия недействительна или истекла")
    return sessions[session_id]

def delete_session(response: Response):
    response.delete_cookie("session_token")


def decode_session_token(token: str) -> dict:
    """Декодирование токена сессии."""
    try:
        data = json.loads(base64.urlsafe_b64decode(token).decode())
        if not all(key in data for key in ["user_id", "role", "email"]):
            raise ValueError("Некорректная структура токена")
        return data
    except json.JSONDecodeError:
        raise HTTPException(status_code=401, detail="Ошибка декодирования токена")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Невалидная сессия: {str(e)}")



def create_session(data: dict, response: Response, session_lifetime: int = 3600):
    """
    Создает сессию и добавляет ее в cookie.
    
    :param data: Данные сессии (например, user_id, role, email).
    :param response: Ответ FastAPI, куда будут добавлены cookie.
    :param session_lifetime: Время жизни сессии в секундах (по умолчанию 3600 секунд = 1 час).
    """
    session_token = base64.urlsafe_b64encode(json.dumps(data).encode()).decode()
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=session_lifetime,
        samesite="Strict",  # Сильная защита от CSRF
        secure=False,  # Включить True в продакшене с HTTPS
    )
