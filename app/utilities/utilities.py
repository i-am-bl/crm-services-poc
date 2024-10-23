from typing import List

import bcrypt
from fastapi import Depends, HTTPException, Response, status
from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256
from pydantic import UUID4

from ..constants import constants as cnst
from ..constants import messages as msg
from ..exceptions import InvalidCredentials
from .logger import logger


class Password:
    pass

    @staticmethod
    def create_hash(password: str):
        return pbkdf2_sha256.hash(secret=password)

    @staticmethod
    def validate_hash(password: str, hash: str):
        if pbkdf2_sha256.verify(secret=password, hash=hash):
            return True
        raise InvalidCredentials()


class Pagination:
    pass

    @staticmethod
    def pagination_offset(page: int, limit: int) -> int:
        offset = (page - 1) * limit
        return offset

    @staticmethod
    def has_more(total_count: int, page: int, limit: int) -> bool:
        return total_count > (page * limit)


class AuthUtils:
    pass

    @staticmethod
    async def set_cookie(response: Response, token: str, sys_user_uuid: UUID4):
        logger.info({"message": str(msg.TOKEN_REFRESH), "sub": str(sys_user_uuid)})
        return response.set_cookie(
            key=cnst.TOKEN_KEY, value=token, httponly=True, secure=True
        )


class DataUtils:
    def __init__(self) -> None:
        pass

    @classmethod
    def m_dumps(cls, data: object):
        return data.model_dump()

    @classmethod
    def m_dumps_unset(cls, data: object):
        return data.model_dump(exclude_unset=True)

    @classmethod
    def set_empty_strs_null(cls, values: object):
        """
        Ignore optional fields == None
        Set field signaled to be reset to None with ""
        """
        items = values.model_dump(exclude_none=True)
        for key in items:
            if items[key] == "":
                items[key] = None
        return items

    @classmethod
    def record_exists(cls, instance: object, exception: Exception) -> bool:
        if instance:
            class_name = exception.__name__
            logger.warning(
                f"Warning: record already exists, a duplicate entry is not allowed for {class_name}"
            )
            raise exception()
        return instance

    @classmethod
    def record_not_exist(cls, instance: object, exception: Exception) -> bool:
        if not instance:
            class_name = exception.__name__
            logger.warning(f"Warning: record not found for {class_name}")
            raise exception()
        return instance
