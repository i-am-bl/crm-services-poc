from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, update, values
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.models.non_individuals as m_non_individuals
import app.schemas.non_individuals as s_non_individuals
from app.database.database import Operations, get_db
from app.services.utilities import DataUtils as di


class NonIndividualsModels:
    non_individuals = m_non_individuals.NonIndividuals


class NonIndividualsStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_by_entity_ni_uuid(entity_uuid: UUID4, non_individual_uuid: UUID4):
            non_individuals = NonIndividualsModels.non_individuals
            statement = Select(non_individuals).where(
                and_(
                    non_individuals.entity_uuid == entity_uuid,
                    non_individuals.uuid == non_individual_uuid,
                )
            )
            return statement

        @staticmethod
        def sel_by_entity_ni_name(entity_uuid: UUID4, name: str):
            non_individuals = NonIndividualsModels.non_individuals
            statement = Select(non_individuals).where(
                and_(
                    non_individuals.entity_uuid == entity_uuid,
                    non_individuals.name == name,
                    non_individuals.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_non_indivs():
            non_individuals = NonIndividualsModels.non_individuals
            statement = Select(non_individuals).where(
                non_individuals.sys_deleted_at == None
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_by_entity_ni_uuid(
            entity_uuid: UUID4, non_individual_uuid: UUID4, non_individual_data: object
        ):
            non_individuals = NonIndividualsModels.non_individuals
            statement = (
                update(non_individuals)
                .where(
                    and_(
                        non_individuals.entity_uuid == entity_uuid,
                        non_individuals.uuid == non_individual_uuid,
                        non_individuals.sys_deleted_at == None,
                    )
                )
                .values(di.set_empty_strs_null(non_individual_data))
                .returning(non_individuals)
            )
            return statement


class NonIndividualsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_non_individual(
            self,
            entity_uuid: UUID4,
            non_individual_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = NonIndividualsStatements.SelStatements.sel_by_entity_ni_uuid(
                entity_uuid=entity_uuid, non_individual_uuid=non_individual_uuid
            )
            non_individual = await Operations.return_one_row(
                service=cnst.NON_INDIVIDUALS_READ_SERV, statement=statement, db=db
            )
            di.record_not_exist(non_individual)
            return non_individual

        async def get_non_individuals(self, db: AsyncSession = Depends(get_db)):
            statement = NonIndividualsStatements.SelStatements.sel_non_indivs()
            non_individual = await Operations.return_all_rows(
                service=cnst.NON_INDIVIDUALS_READ_SERV, statement=statement, db=db
            )
            di.record_not_exist(non_individual)
            return non_individual

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_non_individual(
            self,
            entity_uuid: UUID4,
            non_individual_data: s_non_individuals.NonIndividualsCreate,
            db: AsyncSession = Depends(get_db),
        ):
            non_individuals = NonIndividualsModels.non_individuals
            statement = NonIndividualsStatements.SelStatements.sel_by_entity_ni_name(
                entity_uuid=entity_uuid, name=non_individual_data.name
            )
            non_individual_exists = Operations.return_one_row(
                service=cnst.NON_INDIVIDUALS_CREATE_SERV, statement=statement, db=db
            )
            di.record_exists(non_individual_exists)
            non_individual = await Operations.add_instance(
                service=cnst.NON_INDIVIDUALS_CREATE_SERV,
                model=non_individuals,
                data=non_individual_data,
                db=db,
            )
            di.record_not_exist(non_individual)
            return non_individual

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_non_individual(
            self,
            entity_uuid: UUID4,
            non_individual_uuid: UUID4,
            non_individual_data: s_non_individuals.NonIndividualsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = (
                NonIndividualsStatements.UpdateStatements.update_by_entity_ni_uuid(
                    entity_uuid=entity_uuid,
                    non_individual_uuid=non_individual_uuid,
                    non_individual_data=non_individual_data,
                )
            )
            non_individual = await Operations.return_one_row(
                service=cnst.NON_INDIVIDUALS_UPDATE_SERV, statement=statement, db=db
            )
            di.rec_not_exist_or_soft_del(non_individual)
            return non_individual

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_non_individual(
            self,
            entity_uuid: UUID4,
            non_individual_uuid: UUID4,
            non_individual_data: s_non_individuals.NonIndividualsDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = (
                NonIndividualsStatements.UpdateStatements.update_by_entity_ni_uuid(
                    entity_uuid=entity_uuid,
                    non_individual_uuid=non_individual_uuid,
                    non_individual_data=non_individual_data,
                )
            )
            non_individual = await Operations.return_one_row(
                service=cnst.NON_INDIVIDUALS_UPDATE_SERV, statement=statement, db=db
            )
            di.record_not_exist(non_individual)
            return non_individual
