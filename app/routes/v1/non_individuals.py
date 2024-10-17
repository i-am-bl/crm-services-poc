from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.non_individuals as s_non_individuals
from app.database.database import get_db
from app.services.non_individuals import NonIndividualsServices

serv_non_indiv_r = NonIndividualsServices.ReadService()
serv_non_indiv_c = NonIndividualsServices.CreateService()
serv_non_indiv_u = NonIndividualsServices.UpdateService()
serv_non_indiv_d = NonIndividualsServices.DelService()


router = APIRouter()
""" get one non_individual """


@router.get(
    "/v1/entity-management/entities/{entity_uuid}/non-individuals/{non_individual_uuid}/",
    response_model=s_non_individuals.NonIndividualsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_non_individual(
    entity_uuid: UUID4, non_individual_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        non_individual = await serv_non_indiv_r.get_non_individual(
            entity_uuid=entity_uuid, non_individual_uuid=non_individual_uuid, db=db
        )
        return non_individual


""" get all non_individuals """


@router.get(
    "/v1/entity-management/entities/non-individuals/",
    response_model=List[s_non_individuals.NonIndividualsResponse],
    status_code=status.HTTP_200_OK,
)
async def get_non_individuals(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        non_individuals = await serv_non_indiv_r.get_non_individuals(db=db)
        return non_individuals


@router.post(
    "/v1/entity-management/entities/{entity_uuid}/non-individuals/",
    response_model=s_non_individuals.NonIndividualsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_non_individual(
    entity_uuid: UUID4,
    non_individual_data: s_non_individuals.NonIndividualsCreate,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        non_individual = await serv_non_indiv_c.create_non_individual(
            entity_uuid=entity_uuid, non_individual_data=non_individual_data, db=db
        )
        return non_individual


@router.put(
    "/v1/entity-management/entities/{entity_uuid}/non-individuals/{non_individual_uuid}/",
    response_model=s_non_individuals.NonIndividualsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_non_individual(
    entity_uuid: UUID4,
    non_individual_uuid: UUID4,
    non_individual_data: s_non_individuals.NonIndividualsUpdate,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        non_individual = await serv_non_indiv_u.update_non_individual(
            entity_uuid=entity_uuid,
            non_individual_uuid=non_individual_uuid,
            non_individual_data=non_individual_data,
            db=db,
        )
        return non_individual


@router.delete(
    "/v1/entity-management/entities/{entity_uuid}/non-individuals/{non_individual_uuid}/",
    response_model=s_non_individuals.NonIndividualsDelResponse,
    status_code=status.HTTP_200_OK,
)
async def get_non_individual(
    entity_uuid: UUID4,
    non_individual_uuid: UUID4,
    non_individual_data: s_non_individuals.NonIndividualsDel,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        non_individual = await serv_non_indiv_d.soft_del_non_individual(
            entity_uuid=entity_uuid,
            non_individual_uuid=non_individual_uuid,
            non_individual_data=non_individual_data,
            db=db,
        )
        return non_individual
