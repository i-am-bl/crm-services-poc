import bcrypt
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256

import app.constants.messages as msg

from .logger import logger


class PasswordUtils:
    def __init__(self) -> None:
        pass

    @staticmethod
    def gen_hash(password: str):
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def validate_hash(password: str, hash: str):
        return pbkdf2_sha256.verify(password, hash)


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
    def soft_deleted(cls, instance: object, exception: Exception):
        if instance.sys_deleted_at:
            logger.warning(
                f"Warning: record does not exist and was removed at {instance.sys_deleted_at}"
            )
            raise exception()
        return True if instance.sys_deleted_at else False

    @classmethod
    def record_exists(cls, instance: object, exception: Exception) -> bool:
        if instance:
            logger.warning(
                f"Warning: record already exists, a duplicate entry is not allowed for {instance}"
            )
            raise exception()

        return True if instance else False

    @classmethod
    def record_not_exist(cls, instance: object, exception: Exception) -> bool:
        if not instance:
            raise exception()
        return True if instance else False
