from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db
from ...schemas import numbers as s_numbers
from ...services.authetication import SessionService
from ...services.numbers import NumbersServices
from ...utilities.service_utils import pagination_offset
from ...utilities.sys_users import SetSys
from ...exceptions import UnhandledException, NumberExists, NumbersNotExist

router = APIRouter()

serv_num_c = NumbersServices.CreateService()
serv_num_r = NumbersServices.ReadService()
serv_num_u = NumbersServices.UpdateService()
serv_num_d = NumbersServices.DelService()
serv_session = SessionService()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/numbers/{number_uuid}/",
    response_model=s_numbers.NumbersResponse,
    status_code=status.HTTP_200_OK,
)
async def get_number(
    request: Request,
    respone: Response,
    entity_uuid: UUID4,
    number_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one number by entity"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=respone, db=db
            )
            number = await serv_num_r.get_number(
                entity_uuid=entity_uuid,
                number_uuid=number_uuid,
                db=db,
            )
            return number
    except NumbersNotExist:
        raise NumbersNotExist()
    except Exception:
        raise UnhandledException()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/numbers/",
    response_model=s_numbers.NumbersPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_numbers(
    request: Request,
    respone: Response,
    entity_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many numbers by entity"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=respone, db=db
            )
            offset = pagination_offset(page=page, limit=limit)
            total_count = await serv_num_r.get_numbers_ct(
                entity_uuid=entity_uuid, db=db
            )
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
    except NumbersNotExist:
        raise NumbersNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/numbers/",
    response_model=s_numbers.NumbersResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_number(
    request: Request,
    respone: Response,
    entity_uuid: UUID4,
    number_data: s_numbers.NumbersCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one number"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=respone, db=db
            )
            SetSys.sys_created_by(data=number_data, sys_user=sys_user)
            number = await serv_num_c.create_num(
                entity_uuid=entity_uuid, number_data=number_data, db=db
            )
            return number
    except NumberExists:
        raise NumberExists()
    except NumbersNotExist:
        raise NumbersNotExist()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/numbers/{number_uuid}/",
    response_model=s_numbers.NumbersResponse,
    status_code=status.HTTP_201_CREATED,
)
async def update_number(
    request: Request,
    respone: Response,
    entity_uuid: UUID4,
    number_uuid: UUID4,
    number_data: s_numbers.NumbersUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one number"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=respone, db=db
            )
            SetSys.sys_updated_by(data=number_data, sys_user=sys_user)
            number = await serv_num_u.update_num(
                entity_uuid=entity_uuid,
                number_uuid=number_uuid,
                number_data=number_data,
                db=db,
            )
            return number
    except NumbersNotExist:
        raise NumbersNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/numbers/{number_uuid}/",
    response_model=s_numbers.NumbersDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_number(
    request: Request,
    respone: Response,
    entity_uuid: UUID4,
    number_uuid: UUID4,
    number_data: s_numbers.NumbersDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one number"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=respone, db=db
            )
            SetSys.sys_deleted_by(data=number_data, sys_user=sys_user)
            number = await serv_num_d.soft_del_num_eng(
                entity_uuid=entity_uuid,
                number_uuid=number_uuid,
                number_data=number_data,
                db=db,
            )
            return number
    except NumbersNotExist:
        raise NumbersNotExist()
    except Exception:
        raise UnhandledException()
