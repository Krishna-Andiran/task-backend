from fastapi import FastAPI
from src.db.config.db import engine, Base  
from src.routes.auth import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)