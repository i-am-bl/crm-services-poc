from datetime import datetime, timedelta, timezone
from functools import wraps
from pydoc import resolve
from typing import Annotated, Any, Callable, Optional
from urllib import response

import jwt
from config import settings as set
from fastapi import Cookie, Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import pbkdf2_sha256
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.database import get_db, transaction_manager
from ..exceptions import InvalidCredentials
from ..schemas import sys_users as s_sys_user
from ..schemas import token as s_token
from ..services.sys_users import SysUsersServices
from ..utilities.logger import logger
from ..utilities.utilities import DataUtils as di

serv_sys_user_r = SysUsersServices.ReadService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=cnst.TOKEN_URL)
# TODO: clean up this file, some of this is deprecated


class PasswordService:
    pass

    @staticmethod
    def create_hash(password: str):
        return pbkdf2_sha256.hash(secret=password)

    @staticmethod
    def validate_hash(password: str, hash: str):
        if pbkdf2_sha256.verify(secret=password, hash=hash):
            return True
        raise InvalidCredentials()


class TokenService:
    def __init__(self) -> None:
        pass

    async def extract_token(self, request: Request):
        return request.cookies.get(cnst.TOKEN_KEY)

    async def set_cookie(self, response: Response, token: str):
        return response.set_cookie(
            key=cnst.TOKEN_KEY, value=token, secure=True, httponly=True
        )

    def set_auth_cookie(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            response = kwargs.get("response")
            user_token = kwargs.get("user_token")
            _, token = user_token
            await self.set_cookie(response=response, token=token)
            return await func(*args, **kwargs)

        return wrapper

    def exp_helper(self, expires_delta: Optional[timedelta] = None):
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        return expire

    async def create_token_context(
        self, sys_user: object, expires_delta: Optional[timedelta] = None
    ):
        token_dict = {}
        token_dict["sub"] = str(sys_user.uuid)
        token_dict["exp"] = self.exp_helper(expires_delta=expires_delta)
        valid_token = s_token.TokenData(**token_dict)
        return di.m_dumps(data=valid_token)

    async def create_access_token(self, token_claims) -> any:
        to_encode = token_claims.copy()
        return jwt.encode(to_encode, set.jwt_secret_key, set.jwt_algorithm)

    async def validate_access_token(
        self, token: str, db: AsyncSession = Depends(get_db)
    ):
        token_data = jwt.decode(token, set.jwt_secret_key, set.jwt_algorithm)

        # TODO: Decoding exceptions
        sys_user = await serv_sys_user_r.get_sys_user_by_uuid(
            sys_user_uuid=token_data.get("sub"), db=db
        )

        if sys_user:
            expires_delta = timedelta(minutes=set.jwt_expiration)
            token_claims = await self.create_token_context(
                sys_user=sys_user, expires_delta=expires_delta
            )
        return sys_user, await self.create_access_token(token_claims=token_claims)


class AuthService:
    def __init__(self) -> None:
        pass

    async def validate_user(
        self, form_data: s_token.TokenRequest, db: AsyncSession = Depends(get_db)
    ):
        sys_user = await serv_sys_user_r.get_sys_user_by_username(
            username=form_data.username, db=db
        )
        if PasswordService.validate_hash(
            password=form_data.password, hash=sys_user.password
        ):
            return sys_user


class SessionService:
    def __init__(self) -> None:
        pass

    async def create_session(
        self, form_data: s_sys_user.SysUserLogin, db: AsyncSession = Depends(get_db)
    ):
        expires_delta = timedelta(minutes=set.jwt_expiration)
        serv_auth = AuthService()
        serv_token = TokenService()
        valid_user = await serv_auth.validate_user(form_data=form_data, db=db)
        if valid_user:
            token_claims = await serv_token.create_token_context(
                sys_user=valid_user, expires_delta=expires_delta
            )
            access_token = await serv_token.create_access_token(
                token_claims=token_claims
            )

            return access_token

    async def validate_session(
        self,
        jwt: str = Cookie(...),
        db: AsyncSession = Depends(get_db),
    ):
        serv_token = TokenService()
        async with transaction_manager(db=db):
            sys_user, valid_token = await serv_token.validate_access_token(
                token=jwt, db=db
            )
            return sys_user, valid_token
