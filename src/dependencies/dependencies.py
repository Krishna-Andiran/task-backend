from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import secrets
from datetime import timedelta, datetime, timezone
from src.db.config.db import get_DB
from starlette import status
from src.util.content import user_not_verified, username as name, uid

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token/")

db_dependency = Annotated[Session, Depends(get_DB)]


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get(name)
        id: int = payload.get(uid)

        if not username or not id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=user_not_verified
            )
        return {name: username, uid: id}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=user_not_verified
        )


user_dependency = Annotated[dict, Depends(get_current_user)]


def create_access_token(username: str, user_id: int, expires_time=timedelta):
    encode = {name: username, uid: user_id}
    expires = datetime.now(timezone.utc) + expires_time
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
