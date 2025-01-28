from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from ._variables import ConstrainedStr, TimeStamp


class WebsitesBase(BaseModel):
    entity_uuid: UUID4
    sys_value_type_uuid: Optional[UUID4] = None
    url: ConstrainedStr
    description: Optional[ConstrainedStr]


class WebsitesCreate(WebsitesBase):
    sys_created_by: Optional[UUID4] = None
    sys_created_at: datetime = TimeStamp


class WebsitesUpdate(BaseModel):
    url: Optional[ConstrainedStr] = None
    description: Optional[ConstrainedStr] = None
    sys_value_type_uuid: Optional[UUID4] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class WebsitesDel(BaseModel):
    sys_deleted_by: Optional[UUID4] = None
    sys_deleted_at: datetime = TimeStamp


class WebsitesRes(BaseModel):
    id: int
    uuid: UUID4
    entity_uuid: UUID4
    sys_value_type_uuid: Optional[UUID4] = None
    url: ConstrainedStr
    description: Optional[ConstrainedStr]
    sys_created_by: Optional[UUID4] = None
    sys_created_at: datetime
    sys_updated_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class WebsitesPgRes(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    websites: Optional[List[WebsitesRes]] = None


class WebsiteDelRes(WebsitesRes):
    sys_deleted_by: Optional[UUID4] = None
    sys_deleted_at: datetime

    class Config:
        from_attributes = True
