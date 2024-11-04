from fastapi import FastAPI
from src.db.config.db import engine, Base
from src.routes import auth_router, web_socket_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(web_socket_router.router)
