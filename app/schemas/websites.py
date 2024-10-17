from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel

from ._variables import ConstrainedStr, TimeStamp


class WebsitesBase(BaseModel):
    entity_uuid: UUID4
    sys_value_type_id: Optional[int] = None
    url: ConstrainedStr
    description: Optional[ConstrainedStr]


class WebsitesCreate(WebsitesBase):
    sys_created_by: Optional[UUID4] = None
    sys_created_at: datetime = TimeStamp


class WebsitesUpdate(BaseModel):
    url: Optional[ConstrainedStr] = None
    description: Optional[ConstrainedStr] = None
    # TODO: once we have reference values in place, refactor this
    sys_value_type_id: Optional[int] = None
    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class WebsitesSoftDel(BaseModel):
    sys_deleted_by: Optional[UUID4] = None
    sys_deleted_at: datetime = TimeStamp


class WebsitesResponse(BaseModel):
    id: int
    uuid: UUID4
    entity_uuid: UUID4
    sys_value_type_id: Optional[int] = None
    url: ConstrainedStr
    description: Optional[ConstrainedStr]
    sys_created_by: Optional[UUID4] = None
    sys_created_at: datetime
    sys_updated_by: Optional[UUID4] = None
    sys_updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class WebsiteDelReponse(WebsitesResponse):
    sys_deleted_by: Optional[UUID4] = None
    sys_deleted_at: datetime

    class Config:
        from_attributes = True
