from fastapi import APIRouter, Depends, Query, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.individuals as s_individuals
from app.database.database import Operations, get_db
from app.services.individuals import IndividualsServices

serv_individuals_r = IndividualsServices.ReadService()
serv_individuals_c = IndividualsServices.CreateService()
serv_individuals_u = IndividualsServices.UpdateService()
serv_individuals_d = IndividualsServices.DelService()

router = APIRouter()


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/individuals/{individual_uuid}/",
    response_model=s_individuals.IndividualsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_individual(
    entity_uuid: UUID4, individual_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    """get one individual"""
    async with db.begin():
        individual = await serv_individuals_r.get_individual(
            entity_uuid=entity_uuid, individual_uuid=individual_uuid, db=db
        )
        return individual


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/individuals/",
    response_model=s_individuals.IndividualsResponse,
    status_code=status.HTTP_200_OK,
)
async def create_individual(
    entity_uuid: UUID4,
    individual_data: s_individuals.IndividualsCreate,
    db: AsyncSession = Depends(get_db),
):
    """create one individual"""
    async with db.begin():
        individual = await serv_individuals_c.create_individual(
            entity_uuid=entity_uuid, individual_data=individual_data, db=db
        )
        return individual


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/individuals/{individual_uuid}/",
    response_model=s_individuals.IndividualsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_individual(
    entity_uuid: UUID4,
    individual_uuid: UUID4,
    individual_data: s_individuals.IndividualsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one individual"""
    async with db.begin():
        individual = await serv_individuals_u.update_individual(
            entity_uuid=entity_uuid,
            individual_uuid=individual_uuid,
            individual_data=individual_data,
            db=db,
        )
        return individual


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/individuals/{individual_uuid}/",
    response_model=s_individuals.IndividualsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_individual(
    entity_uuid: UUID4,
    individual_uuid: UUID4,
    individual_data: s_individuals.IndividualsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one entity"""
    async with db.begin():
        individual = await serv_individuals_d.soft_del_individual(
            entity_uuid=entity_uuid,
            individual_uuid=individual_uuid,
            individual_data=individual_data,
            db=db,
        )
        return individual
