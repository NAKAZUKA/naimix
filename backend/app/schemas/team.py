from typing import Optional
from pydantic import BaseModel, EmailStr

class TeamCreate(BaseModel):
    id_worker: Optional[int]
    title: Optional[str]
    email: Optional[EmailStr]
    discription: Optional[str]
    id_hr: Optional[int]

class TeamResponse(BaseModel):
    id_team: int
    id_worker: Optional[int]
    title: Optional[str]
    email: Optional[EmailStr]
    discription: Optional[str]
    id_hr: Optional[int]

    class Config:
        orm_mode = True
