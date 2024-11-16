from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamResponse
from app.database import get_db

team_router = APIRouter(prefix="/team", tags=["Team"])

# Создать новую команду
@team_router.post("/", response_model=TeamResponse, status_code=201)
async def create_team(team: TeamCreate, db: AsyncSession = Depends(get_db)):
    new_team = Team(**team.dict())
    db.add(new_team)
    await db.commit()
    await db.refresh(new_team)
    return new_team

# Получить команду по ID
@team_router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Team).where(Team.id_team == team_id))
    team = query.scalars().first()
    if not team:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    return team

# Получить список всех команд
@team_router.get("/", response_model=list[TeamResponse])
async def get_all_teams(db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Team))
    teams = query.scalars().all()
    return teams

# Обновить информацию о команде
@team_router.put("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: int, team_data: TeamCreate, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Team).where(Team.id_team == team_id))
    team = query.scalars().first()
    if not team:
        raise HTTPException(status_code=404, detail="Команда не найдена")

    for key, value in team_data.dict(exclude_unset=True).items():
        setattr(team, key, value)

    db.add(team)
    await db.commit()
    await db.refresh(team)
    return team

# Удалить команду
@team_router.delete("/{team_id}", status_code=204)
async def delete_team(team_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Team).where(Team.id_team == team_id))
    team = query.scalars().first()
    if not team:
        raise HTTPException(status_code=404, detail="Команда не найдена")

    await db.delete(team)
    await db.commit()
    return {"detail": "Команда успешно удалена"}
