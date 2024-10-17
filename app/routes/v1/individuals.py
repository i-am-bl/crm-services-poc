from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db
from ...schemas import individuals as s_individuals
from ...services.authetication import SessionService
from ...services.individuals import IndividualsServices
from ...utilities.sys_users import SetSys
from ...exceptions import UnhandledException, IndividualNotExist, IndividualExists

serv_individuals_r = IndividualsServices.ReadService()
serv_individuals_c = IndividualsServices.CreateService()
serv_individuals_u = IndividualsServices.UpdateService()
serv_individuals_d = IndividualsServices.DelService()
serv_session = SessionService()


router = APIRouter()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/individuals/{individual_uuid}/",
    response_model=s_individuals.IndividualsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_individual(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    individual_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """get one individual"""
    try:
        async with db.begin():
            _ = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            individual = await serv_individuals_r.get_individual(
                entity_uuid=entity_uuid, individual_uuid=individual_uuid, db=db
            )
            return individual
    except IndividualNotExist:
        raise IndividualNotExist()
    except Exception:
        raise UnhandledException()


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/individuals/",
    response_model=s_individuals.IndividualsResponse,
    status_code=status.HTTP_200_OK,
)
async def create_individual(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    individual_data: s_individuals.IndividualsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one individual"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_created_by(data=individual_data, sys_user=sys_user)
            individual = await serv_individuals_c.create_individual(
                entity_uuid=entity_uuid, individual_data=individual_data, db=db
            )
            return individual
    except IndividualNotExist:
        raise IndividualNotExist()
    except IndividualExists:
        raise IndividualExists()
    except Exception:
        raise UnhandledException()


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/individuals/{individual_uuid}/",
    response_model=s_individuals.IndividualsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_individual(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    individual_uuid: UUID4,
    individual_data: s_individuals.IndividualsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one individual"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_updated_by(data=individual_data, sys_user=sys_user)
            individual = await serv_individuals_u.update_individual(
                entity_uuid=entity_uuid,
                individual_uuid=individual_uuid,
                individual_data=individual_data,
                db=db,
            )
            return individual
    except IndividualNotExist:
        raise IndividualNotExist()
    except Exception:
        raise UnhandledException()


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/individuals/{individual_uuid}/",
    response_model=s_individuals.IndividualsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_individual(
    request: Request,
    response: Response,
    entity_uuid: UUID4,
    individual_uuid: UUID4,
    individual_data: s_individuals.IndividualsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one entity"""
    try:
        async with db.begin():
            sys_user = await serv_session.validate_session(
                request=request, response=response, db=db
            )
            SetSys.sys_deleted_by(data=individual_data, sys_user=sys_user)
            individual = await serv_individuals_d.soft_del_individual(
                entity_uuid=entity_uuid,
                individual_uuid=individual_uuid,
                individual_data=individual_data,
                db=db,
            )
            return individual
    except IndividualNotExist:
        raise IndividualNotExist()
    except Exception:
        raise UnhandledException()
