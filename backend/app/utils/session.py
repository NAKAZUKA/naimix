import uuid
from fastapi import HTTPException, Request, Response
from typing import Any, Dict
import base64
import json

# Хранилище сессий (в памяти)
sessions: Dict[str, Dict[str, Any]] = {}


def get_session(request: Request) -> dict:
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Сессия недействительна")
    
    try:
        session_data = decode_session_token(session_token)
        print("Decoded session data:", session_data)
        return session_data
    except Exception as e:
        print("Session decoding failed:", str(e))
        raise HTTPException(status_code=401, detail="Сессия недействительна")



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
    session_token = base64.urlsafe_b64encode(json.dumps(data).encode()).decode()
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=session_lifetime,
        samesite="None",  # Для межсайтового контекста
        secure=False,     # Для локальной разработки
    )
