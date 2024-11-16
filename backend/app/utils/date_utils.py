from datetime import datetime

def prepare_birthday(birthday_str: str) -> datetime:
    """
    Конвертирует строку ISO 8601 в naive datetime (без временной зоны).
    """
    birthday_with_tz = datetime.fromisoformat(birthday_str.replace('Z', '+00:00'))
    # Убираем временную зону, чтобы сохранить в формате без временной зоны
    return birthday_with_tz.replace(tzinfo=None)
