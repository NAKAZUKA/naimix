import uuid
from fastapi import HTTPException, Request, Response
from typing import Any, Dict
import base64
import json

# Хранилище сессий (в памяти)
sessions: Dict[str, Dict[str, Any]] = {}


def get_session(request: Request) -> dict:
    session_token = request.cookies.get("session_token")
    print(f"Session token received: {session_token}")  # Логируем полученный токен
    if not session_token:
        print("Session token is missing")
        raise HTTPException(status_code=401, detail="Сессия недействительна")
    
    try:
        session_data = decode_session_token(session_token)
        print(f"Decoded session data: {session_data}")  # Логируем расшифрованные данные
        return session_data
    except Exception as e:
        print(f"Session decoding failed: {e}")
        raise HTTPException(status_code=401, detail="Сессия недействительна")


def delete_session(response: Response):
    response.delete_cookie("session_token")


def decode_session_token(token: str) -> dict:
    try:
        print(f"Decoding token: {token}")
        data = json.loads(base64.urlsafe_b64decode(token).decode())
        print(f"Decoded token data: {data}")
        if not all(key in data for key in ["user_id", "role", "email"]):
            raise ValueError("Некорректная структура токена")
        return data
    except json.JSONDecodeError:
        print("Token decoding error: invalid JSON")
        raise HTTPException(status_code=401, detail="Ошибка декодирования токена")
    except Exception as e:
        print(f"Unexpected error while decoding token: {e}")
        raise HTTPException(status_code=401, detail=f"Невалидная сессия: {str(e)}")




def create_session(data: dict, response: Response, session_lifetime: int = 3600):
    session_token = base64.urlsafe_b64encode(json.dumps(data).encode()).decode()
    print(f"Creating session with data: {data}")
    print(f"Generated token: {session_token}")
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=session_lifetime,
        samesite="None",  # Для межсайтового контекста
        secure=False,     # Для локальной разработки
    )
