from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

import app.models.individuals as m_individuals
import app.schemas.individuals as s_individuals

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..exceptions import IndividualExists, IndividualNotExist
from ..utilities.logger import logger
from ..utilities.utilities import DataUtils as di


class IndividualsModels:
    individuals = m_individuals.Individuals


class IndividualsStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_entity_indiv_uuid(entity_uuid: UUID4):
            individuals = IndividualsModels.individuals
            statement = Select(individuals).where(
                and_(
                    individuals.entity_uuid == entity_uuid,
                    individuals.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_indivs(offset: int, limit: int):
            individuals = IndividualsModels.individuals
            statement = (
                Select(individuals)
                .where(
                    individuals.sys_deleted_at == None,
                )
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_indivs_ct():
            individuals = IndividualsModels.individuals
            statement = (
                Select(func.count())
                .select_from(individuals)
                .where(
                    individuals.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_entity_indiv(entity_uuid: UUID4):
            individuals = IndividualsModels.individuals
            statement = Select(individuals).where(
                and_(
                    individuals.entity_uuid == entity_uuid,
                    individuals.sys_deleted_at == None,
                )
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_entity_indiv_uuid(entity_uuid: UUID4, individual_data: object):
            individuals = IndividualsModels.individuals
            statement = (
                update(individuals)
                .where(
                    and_(
                        individuals.entity_uuid == entity_uuid,
                        individuals.sys_deleted_at == None,
                    )
                )
                .values(di.set_empty_strs_null(individual_data))
            ).returning(individuals)
            return statement


class IndividualsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_individual(
            self,
            entity_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = IndividualsStatements.SelStatements.sel_entity_indiv(
                entity_uuid=entity_uuid
            )
            individual = await Operations.return_one_row(
                service=cnst.INDIVIDUALS_READ_SERV, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=individual, exception=IndividualNotExist
            )

        async def get_individuals(
            self,
            offset: int,
            limit: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = IndividualsStatements.SelStatements.sel_indivs(
                offset=offset, limit=limit
            )
            individual = await Operations.return_all_rows(
                service=cnst.INDIVIDUALS_READ_SERV, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=individual, exception=IndividualNotExist
            )

        async def get_individuals_ct(
            self,
            db: AsyncSession = Depends(get_db),
        ):
            statement = IndividualsStatements.SelStatements.sel_indivs_ct()
            return await Operations.return_count(
                service=cnst.INDIVIDUALS_READ_SERV, statement=statement, db=db
            )

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_individual(
            self,
            entity_uuid: UUID4,
            individual_data: s_individuals.IndividualsCreate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = IndividualsStatements.SelStatements.sel_entity_indiv(
                entity_uuid=entity_uuid
            )
            individuals = IndividualsModels.individuals
            individual_exists = await Operations.return_one_row(
                service=cnst.INDIVIDUALS_CREATE_SERV, statement=statement, db=db
            )
            di.record_exists(instance=individual_exists, exception=IndividualExists)
            individual = await Operations.add_instance(
                service=cnst.INDIVIDUALS_CREATE_SERV,
                model=individuals,
                data=individual_data,
                db=db,
            )
            return di.record_not_exist(
                instance=individual, exception=IndividualNotExist
            )

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_individual(
            self,
            entity_uuid: UUID4,
            individual_data: s_individuals.IndividualsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = IndividualsStatements.UpdateStatements.update_entity_indiv_uuid(
                entity_uuid=entity_uuid,
                individual_data=individual_data,
            )
            individual = await Operations.return_one_row(
                service=cnst.INDIVIDUALS_UPDATE_SERV, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=individual, exception=IndividualNotExist
            )

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_individual(
            self,
            entity_uuid: UUID4,
            individual_data: s_individuals.IndividualsDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = IndividualsStatements.UpdateStatements.update_entity_indiv_uuid(
                entity_uuid=entity_uuid,
                individual_data=individual_data,
            )
            individual = await Operations.return_one_row(
                service=cnst.INDIVIDUALS_DEL_SERV, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=individual, exception=IndividualNotExist
            )
