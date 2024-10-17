import re
from datetime import datetime
from typing import List, Optional
from uuid import uuid5

from pydantic import UUID4, BaseModel, field_validator

from app.schemas._variables import ConstrainedEmailStr, ConstrainedStr, TimeStamp


class SysUsers(BaseModel):
    first_name: ConstrainedStr
    last_name: ConstrainedStr
    email: ConstrainedEmailStr
    username: ConstrainedStr

    @field_validator("email")
    def normalize_email(cls, value):
        return value.lower()

    @field_validator("username")
    def normalize_email(cls, value):
        return value.lower()


class SysUsersCreate(SysUsers):
    password: ConstrainedStr

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if len(value) > 30:
            raise ValueError("Password must be at less than 30 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one numerical character.")
        # TODO: Special characters causing unicode issues
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        #     raise ValueError("Password must contain at least one special character.")
        return value


class SysUsersUpdate(BaseModel):
    first_name: Optional[ConstrainedStr] = None
    last_name: Optional[ConstrainedStr] = None
    email: Optional[ConstrainedEmailStr] = None
    username: Optional[ConstrainedStr] = None
    password: Optional[ConstrainedStr] = None
    sys_updated_at: datetime = TimeStamp

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if len(value) > 30:
            raise ValueError("Password must be at less than 30 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one numerical character.")
        # TODO: Special characters causing unicode issues
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        #     raise ValueError("Password must contain at least one special character.")

        return value


class SysUsersDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[int] = None


class SysUsersDisable(BaseModel):
    disabled_at: datetime = TimeStamp


class SysUsersResponse(BaseModel):
    id: int
    uuid: UUID4
    first_name: ConstrainedStr
    last_name: ConstrainedStr
    email: ConstrainedEmailStr
    username: ConstrainedStr
    sys_created_at: datetime
    sys_created_by: Optional[int] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[int] = None

    class Config:
        from_attributes = True


class SysUsersPagResponse(BaseModel):
    total: int
    page: int
    limit: int
    sys_users: Optional[List[SysUsersResponse]] = None


class SysUsersDelResponse(SysUsersResponse):
    sys_deleted_at: datetime
    sys_deleted_by: Optional[int] = None


class SysUserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sys_user_id: str
    username: str
