from src.db.config.db import Base
from sqlalchemy import Column, String, Integer

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True)
    password = Column(String)