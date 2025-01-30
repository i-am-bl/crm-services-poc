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
from ..utilities.password import validate_hash
from ..utilities.data import m_dumps

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=cnst.TOKEN_URL)


class TokenSrvc:
    """
    Service for managing user authentication, session creation, and token validation.

    This service provides functionality for creating and validating JWT access tokens,
    handling user login sessions, and ensuring secure token-based authentication.

    :param sys_user_read_srvc: Service to read system user data.
    :type sys_user_read_srvc: ReadSrvc
    """

    def __init__(self, sys_user_read_srvc: ReadSrvc):
        """
        Initializes the TokenSrvc class with the provided system user read service.

        :param sys_user_read_srvc: Service to read system user data.
        :type sys_user_read_srvc: ReadSrvc
        """
        self._sys_user_read_srvc: ReadSrvc = sys_user_read_srvc

    @property
    def sys_user_read_srvc(self) -> ReadSrvc:
        """
        Returns the instance of ReadSrvc.

        :returns: The system user read service.
        :rtype: ReadSrvc
        """
        return self._sys_user_read_srvc

    def _context_helper(self, expires_delta: Optional[timedelta] = None):
        """
        Helper function to calculate the expiration time for a token.

        :param expires_delta: The amount of time to add to the current time for expiration.
        :type expires_delta: Optional[timedelta], optional
        :returns: The expiration time for the token.
        :rtype: datetime
        """
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        return expire

    async def _create_token_context(
        self, sys_user: object, expires_delta: Optional[timedelta] = None
    ):
        """
        Creates the token context, including user information and expiration time.

        :param sys_user: The system user to include in the token context.
        :type sys_user: object
        :param expires_delta: The expiration time for the token.
        :type expires_delta: Optional[timedelta], optional
        :returns: The encoded token context as a JSON string.
        :rtype: str
        """
        token_dict = {}
        token_dict["sub"] = str(sys_user.uuid)
        token_dict["exp"] = self._context_helper(expires_delta=expires_delta)
        valid_token = TokenData(**token_dict)
        return m_dumps(data=valid_token)

    async def _create_access_token(self, token_claims) -> any:
        """
        Creates an access token by encoding the token claims using the JWT secret key.

        :param token_claims: The claims (payload) to be encoded into the token.
        :type token_claims: dict
        :returns: The generated access token.
        :rtype: any
        """
        to_encode = token_claims.copy()
        return jwt.encode(to_encode, set.jwt_secret_key, set.jwt_algorithm)

    async def _validate_user(self, form_data: TokenRequest, db: AsyncSession):
        """
        Validates the user by checking the provided credentials against the database.

        :param form_data: The login form data containing the username and password.
        :type form_data: TokenRequest
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession
        :returns: The system user if valid credentials are provided.
        :rtype: SysUsersRes
        :raises: InvalidCredentials if the credentials are incorrect.
        """
        sys_user = await self._sys_user_read_srvc.get_sys_user_by_username(
            username=form_data.username, db=db
        )
        if validate_hash(password=form_data.password, hash=sys_user.password):
            return sys_user

    async def create_session(self, form_data: SysUserLogin, db: AsyncSession):
        """
        Creates a session for the user by validating their credentials and generating an access token.

        :param form_data: The login form data containing the username and password.
        :type form_data: SysUserLogin
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession
        :returns: The generated JWT access token.
        :rtype: any
        :raises: InvalidCredentials if the user cannot be authenticated.
        """
        expires_delta = timedelta(minutes=set.jwt_expiration)

        valid_user = await self._validate_user(form_data=form_data, db=db)
        if valid_user:
            token_claims = await self._create_token_context(
                sys_user=valid_user, expires_delta=expires_delta
            )
            return await self._create_access_token(token_claims=token_claims)

    async def _validate_access_token(self, token: TokenData, db: AsyncSession):
        """
        Validates an access token by decoding it and ensuring the user exists in the system.

        :param token: The access token to be validated.
        :type token: TokenData
        :param db: The asynchronous session for database operations.
        :type db: AsyncSession
        :returns: The system user and a new valid access token.
        :rtype: tuple(SysUsersRes, any)
        :raises: SysUserNotExist if the user does not exist.
        """
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
        """
        Validates the user's session by verifying the provided JWT.

        :param db: The asynchronous session for database operations.
        :type db: AsyncSession
        :param jwt: The JWT token provided in the request cookie.
        :type jwt: str
        :returns: The system user and a valid access token.
        :rtype: tuple(SysUsersRes, any)
        :raises: SysUserNotExist if the user does not exist.
        """
        async with transaction_manager(db=db):
            sys_user, valid_token = await self._validate_access_token(token=jwt, db=db)
            return sys_user, valid_token


def set_auth_cookie(func: Callable) -> Callable:
    """
    Decorator for setting the authentication token in the response cookies.

    This decorator is used to add the authentication token to the HTTP response,
    making it available for future requests.

    :param func: The function to be decorated.
    :type func: Callable
    :returns: The wrapped function with the authentication cookie set.
    :rtype: Callable
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        async def set_cookie(self, response: Response, token: str):
            """
            Helper function to set the cookie in the response.

            :param response: The response object.
            :type response: Response
            :param token: The JWT token to set in the cookie.
            :type token: str
            :returns: The response with the token set as a cookie.
            :rtype: Response
            """
            return response.set_cookie(
                key=cnst.TOKEN_KEY, value=token, secure=True, httponly=True
            )

        response = kwargs.get("response")
        user_token = kwargs.get("user_token")
        _, token = user_token
        await set_cookie(response=response, token=token)
        return await func(*args, **kwargs)

    return wrapper
