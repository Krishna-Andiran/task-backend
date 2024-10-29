from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker, declarative_base

URL_DATABASE = "postgresql://postgres:2004@localhost:3000/task"

engine = create_engine(URL_DATABASE)

SessionLocal =  sessionmaker(autoflush=False,bind=engine)

Base = declarative_base()

def get_DB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()