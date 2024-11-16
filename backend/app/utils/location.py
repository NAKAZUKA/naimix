import requests
from fastapi import HTTPException

def get_coordinates(city_name: str):
    """Получает координаты города через API геолокации."""
    response = requests.get(
        "http://api.positionstack.com/v1/forward",
        params={
            "access_key": "36ca24556bd23d838380b6e062e013a1",  # Ваш API-ключ
            "query": city_name,  # Название города (можно на русском)
        },
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Ошибка при запросе API геолокации")

    data = response.json()
    if not data.get("data"):
        raise HTTPException(status_code=400, detail=f"Город '{city_name}' не найден")

    # Берем первый результат
    location = data["data"][0]
    return {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    }
