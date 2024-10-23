from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from ._variables import ConstrainedEmailStr, TimeStamp


class Emails(BaseModel):
    email: ConstrainedEmailStr


class EmailsCreate(Emails):
    entity_uuid: UUID4
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class EmailsUpdate(BaseModel):
    email: Optional[ConstrainedEmailStr] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class EmailsDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class EmailsRespone(BaseModel):
    id: int
    uuid: UUID4
    entity_uuid: UUID4
    sys_created_at: datetime
    sys_created_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime] = None
    sys_updated_by: Optional[UUID4] = None

    class Config:
        from_attributes: True


class EmailsPagRespone(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    emails: Optional[List[EmailsRespone]] = None

    class Config:
        from_attributes: True


class EmailsDelResponse(EmailsRespone):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes: True
