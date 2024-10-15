from typing import Annotated, List, Optional

import bcrypt
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.messages as msg
import app.schemas.entities as s_ent
import app.schemas.individuals as s_indiv
import app.schemas.non_individuals as s_non_indiv
from app.logger import logger


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
    def soft_deleted(cls, model: object):
        if model.sys_deleted_at:
            logger.warning(
                f"Warning: record does not exist and was removed at {model.sys_deleted_at}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg.RECORD_NOT_EXIST,
            )
        return True if model.sys_deleted_at else False

    @classmethod
    def record_exists(cls, model: object) -> bool:
        if model:
            logger.warning(
                f"Warning: record already exists, a duplicate entry is not allowed for {model}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg.RECORD_EXISTS,
            )

        return True if model else False

    # TODO: Refacthis to be instance instead of model.. confusing I think
    @classmethod
    def record_not_exist(cls, model: object) -> bool:
        if not model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg.RECORD_NOT_EXIST,
            )
        return True if model else False

    @classmethod
    def rec_not_exist_or_soft_del(cls, model: object) -> None:
        cls.record_not_exist(model)
        cls.soft_deleted(model)
