from fastapi import APIRouter, Depends, Query, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.schemas.numbers as s_numbers
from app.database.database import get_db
from app.services.numbers import NumbersServices
from app.services.utilities import DataUtils as di
from app.service_utils import pagination_offset

router = APIRouter()

serv_num_c = NumbersServices.CreateService()
serv_num_r = NumbersServices.ReadService()
serv_num_u = NumbersServices.UpdateService()
serv_num_d = NumbersServices.DelService()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/numbers/{number_uuid}/",
    response_model=s_numbers.NumbersResponse,
    status_code=status.HTTP_200_OK,
)
async def get_number(
    entity_uuid: UUID4, number_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    """get one number by entity"""
    async with db.begin():
        number = await serv_num_r.get_num(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            db=db,
        )
        return number


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/numbers/",
    response_model=s_numbers.NumbersPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_numbers(
    entity_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many numbers by entity"""
    async with db.begin():
        offset = pagination_offset(page=page, limit=limit)
        total_count = await serv_num_r.get_numbers_ct(entity_uuid=entity_uuid, db=db)
        numbers = await serv_num_r.get_numbers(
            entity_uuid=entity_uuid,
            limit=limit,
            offset=offset,
            db=db,
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": total_count > (page * limit),
            "numbers": numbers,
        }


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/numbers/",
    response_model=s_numbers.NumbersResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_number(
    entity_uuid: UUID4,
    number_data: s_numbers.NumbersCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one number"""
    async with db.begin():
        number = await serv_num_c.create_num(
            entity_uuid=entity_uuid, number_data=number_data, db=db
        )
        return number


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/numbers/{number_uuid}/",
    response_model=s_numbers.NumbersResponse,
    status_code=status.HTTP_201_CREATED,
)
async def update_number(
    entity_uuid: UUID4,
    number_uuid: UUID4,
    number_data: s_numbers.NumbersUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one number"""
    async with db.begin():
        number = await serv_num_u.update_num(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            number_data=number_data,
            db=db,
        )
        return number


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/numbers/{number_uuid}/",
    response_model=s_numbers.NumbersDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_number(
    entity_uuid: UUID4,
    number_uuid: UUID4,
    number_data: s_numbers.NumbersDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one number"""
    async with db.begin():
        number = await serv_num_d.soft_del_num_eng(
            entity_uuid=entity_uuid,
            number_uuid=number_uuid,
            number_data=number_data,
            db=db,
        )
        return number
