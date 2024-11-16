from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Team(Base):
    __tablename__ = "TEAM"

    id_team = Column(Integer, primary_key=True, index=True)
    id_worker = Column(Integer, ForeignKey("USERS.id"), nullable=True)  # Связь с работником
    title = Column(Text, nullable=True)  # Название команды
    email = Column(Text, nullable=True)  # Email команды
    discription = Column(Text, nullable=True)  # Описание команды
    id_hr = Column(Integer, ForeignKey("USERS.id"), nullable=True)  # Связь с HR

    # Определяем связи с таблицей USERS
    hr = relationship("User", foreign_keys=[id_hr])  # Связь с HR
    worker = relationship("User", foreign_keys=[id_worker])  # Связь с работником
