import uuid
from fastapi import HTTPException, Request, Response
from typing import Any, Dict

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

def delete_session(request: Request, response: Response):
    """Удаляет текущую сессию."""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        del sessions[session_id]
    response.delete_cookie("session_id")
