from datetime import UTC, datetime, timedelta, timezone

import jwt
from config import settings as set
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/system-management/login/")


class AuthService:
    def __init__(self) -> None:
        pass

    @staticmethod
    async def gen_access_token(data: dict, expires_delta: timedelta | None = None):

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, set.jwt_secret_key, set.jwt_algorithm)

        return encoded_jwt

    # TODO: review validation process
    @staticmethod
    async def verify_access_token(token: str, credentials_exception):
        payload = jwt.decode(token, set.jwt_secret_key, set.jwt_algorithm)
        sys_user_uuid = payload.get("sys_user_uuid")
        if not sys_user_uuid:
            raise credentials_exception
        # TODO: add additional validation

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"could not validate",
            headers={"WWW-Athenticate": "Bearer"},
        )
        return AuthService.verify_access_token(
            token=token, credentials_exception=credentials_exception
        )
