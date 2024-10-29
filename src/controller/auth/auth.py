from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from src.db.models.user import User
from src.db.pymodels.user import CreateUserRequest
from src.util.content import (
    status as st,
    success,
    data,
    bearer,
    access_token,
    token_type,
    user_not_verified,
    internal,
    authentication_failed,
)
from datetime import timedelta

from src.dependencies.dependencies import (
    db_dependency,
    user_dependency,
    create_access_token,
    bcrypt_context,
)


def create_user(db: db_dependency, create_user: CreateUserRequest):
    try:
        create_user_model = User(
            username=create_user.username,
            password=bcrypt_context.hash(create_user.password),
        )
        db.add(create_user_model)
        db.commit()
        return {
            st: success,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    try:
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=user_not_verified
            )
        token = create_access_token(user.username, user.id, timedelta(minutes=20))
        return {access_token: token, token_type: bearer}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def authenticate_user(username: str, password: str, db):
    try:
        user = db.query(User).filter(User.username == username).first()

        if not user:
            return False
        if not bcrypt_context.verify(password, user.password):
            return False
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def get_user(db: db_dependency, user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail=authentication_failed)
        if db is None:
            raise HTTPException(status_code=500, detail=internal)
        return {st: success, data: user}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
