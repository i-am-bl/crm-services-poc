from curses import intrflush
from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import UUID4, BaseModel, StringConstraints

from ._variables import ConstrainedStr, TimeStamp


class Numbers(BaseModel):
    entity_uuid: UUID4
    country_code: Annotated[
        ConstrainedStr, StringConstraints(min_length=1, max_length=1)
    ] = None
    area_code: Annotated[
        ConstrainedStr, Optional[StringConstraints(min_length=3, max_length=3)]
    ] = None
    line_number: Annotated[
        ConstrainedStr, Optional[StringConstraints(min_length=4, max_length=4)]
    ] = None
    extension: Optional[ConstrainedStr] = None


class NumbersCreate(Numbers):
    sys_created_at: datetime = TimeStamp
    sys_created_by: Optional[UUID4] = None


class NumbersUpdate(BaseModel):
    country_code: Annotated[
        ConstrainedStr, Optional[StringConstraints(min_length=1, max_length=1)]
    ]

    area_code: Annotated[ConstrainedStr, StringConstraints(min_length=3, max_length=3)]
    line_number: Annotated[
        ConstrainedStr, StringConstraints(min_length=4, max_length=4)
    ]
    extension: Optional[ConstrainedStr] = None

    sys_updated_at: datetime = TimeStamp
    sys_updated_by: Optional[UUID4] = None


class NumbersDel(BaseModel):
    sys_deleted_at: datetime = TimeStamp
    sys_deleted_by: Optional[UUID4] = None


class NumbersRes(BaseModel):
    id: int
    uuid: UUID4
    entity_uuid: UUID4
    country_code: Optional[str] = None
    area_code: Optional[str] = None
    line_number: Optional[str] = None
    extension: Optional[str] = None

    class Config:
        from_attributes: True


class NumbersPgRes(BaseModel):
    total: int
    page: int
    limit: int
    has_more: bool
    numbers: Optional[List[NumbersRes]] = None


class NumbersDelRes(Numbers):
    id: int
    uuid: UUID4
    entity_uuid: UUID4
    sys_deleted_at: datetime
    sys_deleted_by: Optional[UUID4] = None

    class Config:
        from_attributes: True
