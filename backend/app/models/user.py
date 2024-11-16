from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY
from app.database import Base

class User(Base):
    __tablename__ = "USERS"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, nullable=False)
    firstname = Column(Text, nullable=True)
    secondname = Column(Text, nullable=True)
    birthday = Column(DateTime, nullable=True)
    role = Column(Text, nullable=True, default="user")
    bio = Column(Text, nullable=True)
    coordinates = Column(ARRAY(Text), nullable=True)
    password = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    phone_number = Column(Text, nullable=True)
    stack = Column(Text, nullable=True)
    position = Column(Text, nullable=True)
    cosmogram = Column(Text, nullable=True)
