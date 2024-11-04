from fastapi import APIRouter, Depends
from starlette import status
from src.db.pymodels.user import CreateUserRequest
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.dependencies.dependencies import db_dependency, user_dependency
from src.controller.auth import create_user as create_user_func, login_for_access_token as login_func, get_user as get_user_func

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(create_user_request: CreateUserRequest, db: db_dependency):
    return create_user_func(db, create_user_request)

@router.post("/token")
async def login_for_access_token_endpoint(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return login_func(form_data, db)

@router.get("/", status_code=status.HTTP_200_OK)
async def user(db: db_dependency, user: user_dependency):
    return get_user_func(db, user)
