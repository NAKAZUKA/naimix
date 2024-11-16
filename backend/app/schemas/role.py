from pydantic import BaseModel

class RoleCreate(BaseModel):
    name: str  # Имя роли
    description: str = ""  # Описание роли (необязательное поле)

class RoleResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
