from datetime import datetime, timedelta, timezone
from fastapi import Cookie
from functools import wraps
from typing import Any, Callable, Optional

import jwt
from config import settings as set
from fastapi import Request, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.database import transaction_manager
from ..schemas.token import TokenData, TokenRequest
from ..schemas.sys_users import SysUserLogin
from ..services.sys_users import ReadSrvc
from ..utilities.utilities import DataUtils as di, Password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=cnst.TOKEN_URL)


class TokenSrvc:
    def __init__(self, sys_user_read_srvc: ReadSrvc):
        self._sys_user_read_srvc: ReadSrvc = sys_user_read_srvc

    @property
    def sys_user_read_srvc(self) -> ReadSrvc:
        return self._sys_user_read_srvc

    def _context_helper(self, expires_delta: Optional[timedelta] = None):
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        return expire

    async def _create_token_context(
        self, sys_user: object, expires_delta: Optional[timedelta] = None
    ):
        token_dict = {}
        token_dict["sub"] = str(sys_user.uuid)
        token_dict["exp"] = self.context_helper(expires_delta=expires_delta)
        valid_token = TokenData(**token_dict)
        return di.m_dumps(data=valid_token)

    async def _create_access_token(self, token_claims) -> any:
        to_encode = token_claims.copy()
        return jwt.encode(to_encode, set.jwt_secret_key, set.jwt_algorithm)

    async def _validate_user(self, form_data: TokenRequest, db: AsyncSession):
        sys_user = await self._sys_user_read_srvc.get_sys_user_by_username(
            username=form_data.username, db=db
        )
        if Password.validate_hash(password=form_data.password, hash=sys_user.password):
            return sys_user

    async def create_session(self, form_data: SysUserLogin, db: AsyncSession):
        expires_delta = timedelta(minutes=set.jwt_expiration)

        valid_user = await self._validate_user(form_data=form_data, db=db)
        if valid_user:
            token_claims = await self._create_token_context(
                sys_user=valid_user, expires_delta=expires_delta
            )
            return await self._create_access_token(token_claims=token_claims)

    async def _validate_access_token(self, token: TokenData, db: AsyncSession):
        token_data: str = jwt.decode(token, set.jwt_secret_key, set.jwt_algorithm)

        sys_user = await self._sys_user_read_srvc.get_sys_user(
            sys_user_uuid=token_data.get("sub"), db=db
        )

        if sys_user:
            expires_delta = timedelta(minutes=set.jwt_expiration)
            token_claims = await self.create_token_context(
                sys_user=sys_user, expires_delta=expires_delta
            )
        return sys_user, await self._create_access_token(token_claims=token_claims)

    async def validate_session(
        self,
        db: AsyncSession,
        jwt: str = Cookie(...),
    ):

        async with transaction_manager(db=db):
            sys_user, valid_token = await self._validate_access_token(token=jwt, db=db)
            return sys_user, valid_token


def set_auth_cookie(self, func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        async def set_cookie(self, response: Response, token: str):
            return response.set_cookie(
                key=cnst.TOKEN_KEY, value=token, secure=True, httponly=True
            )

        response = kwargs.get("response")
        user_token = kwargs.get("user_token")
        _, token = user_token
        await set_cookie(response=response, token=token)
        return await func(*args, **kwargs)

    return wrapper
