from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..exceptions import NonIndividualExists, NonIndividualNotExist
from ..models import non_individuals as m_non_individuals
from ..schemas import non_individuals as s_non_individuals
from ..utilities.utilities import DataUtils as di


class NonIndividualsModels:
    non_individuals = m_non_individuals.NonIndividuals


class NonIndividualsStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_by_entity_ni(entity_uuid: UUID4):
            non_individuals = NonIndividualsModels.non_individuals
            statement = Select(non_individuals).where(
                and_(
                    non_individuals.entity_uuid == entity_uuid,
                    non_individuals.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_non_indivs(offset: int, limit: int):
            non_individuals = NonIndividualsModels.non_individuals
            statement = (
                Select(non_individuals)
                .where(
                    non_individuals.sys_deleted_at == None,
                )
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_non_indivs_ct():
            non_individuals = NonIndividualsModels.non_individuals
            statement = (
                Select(func.count())
                .select_from(non_individuals)
                .where(
                    non_individuals.sys_deleted_at == None,
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

    class UpdateStatements:
        pass

        @staticmethod
        def update_by_entity_ni_uuid(entity_uuid: UUID4, non_individual_data: object):
            non_individuals = NonIndividualsModels.non_individuals
            statement = (
                update(non_individuals)
                .where(
                    and_(
                        non_individuals.entity_uuid == entity_uuid,
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
            db: AsyncSession = Depends(get_db),
        ):
            statement = NonIndividualsStatements.SelStatements.sel_by_entity_ni(
                entity_uuid=entity_uuid
            )
            non_individual = await Operations.return_one_row(
                service=cnst.NON_INDIVIDUALS_READ_SERV, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=non_individual, exception=NonIndividualNotExist
            )

        async def get_non_individuals(
            self, offset: int, limit: int, db: AsyncSession = Depends(get_db)
        ):
            statement = NonIndividualsStatements.SelStatements.sel_non_indivs(
                offset=offset, limit=limit
            )
            non_individual = await Operations.return_all_rows(
                service=cnst.NON_INDIVIDUALS_READ_SERV, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=non_individual, exception=NonIndividualNotExist
            )

        async def get_non_individuals_ct(
            self, offset: int, limit: int, db: AsyncSession = Depends(get_db)
        ):
            statement = NonIndividualsStatements.SelStatements.sel_non_indivs_ct()
            return await Operations.return_count(
                service=cnst.NON_INDIVIDUALS_READ_SERV, statement=statement, db=db
            )

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
            non_individual_exists = await Operations.return_one_row(
                service=cnst.NON_INDIVIDUALS_CREATE_SERV, statement=statement, db=db
            )
            di.record_exists(
                instance=non_individual_exists, exception=NonIndividualExists
            )
            non_individual = await Operations.add_instance(
                service=cnst.NON_INDIVIDUALS_CREATE_SERV,
                model=non_individuals,
                data=non_individual_data,
                db=db,
            )
            return di.record_not_exist(
                instance=non_individual, exception=NonIndividualNotExist
            )

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_non_individual(
            self,
            entity_uuid: UUID4,
            non_individual_data: s_non_individuals.NonIndividualsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = (
                NonIndividualsStatements.UpdateStatements.update_by_entity_ni_uuid(
                    entity_uuid=entity_uuid,
                    non_individual_data=non_individual_data,
                )
            )
            non_individual = await Operations.return_one_row(
                service=cnst.NON_INDIVIDUALS_UPDATE_SERV, statement=statement, db=db
            )
            return di.record_not_exist(
                instance=non_individual, exception=NonIndividualNotExist
            )

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
            return di.record_not_exist(
                instance=non_individual, exception=NonIndividualNotExist
            )
