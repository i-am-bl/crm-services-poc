from typing import Optional

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..exceptions import NumberExists, NumbersNotExist
from ..models import numbers as m_numbers
from ..schemas import numbers as s_numbers
from ..utilities.utilities import DataUtils as di


class NumbersModels:
    numbers = m_numbers.Numbers


class NumbersStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_num_by_uuid(entity_uuid: UUID4, number_uuid: UUID4):
            numbers = NumbersModels.numbers
            statement = Select(numbers).where(
                and_(
                    numbers.entity_uuid == entity_uuid,
                    numbers.uuid == number_uuid,
                )
            )

            return statement

        @staticmethod
        def sel_num_by_entity(
            entity_uuid: UUID4,
            limit: int,
            offset: int,
        ):
            numbers = NumbersModels.numbers
            statement = (
                Select(numbers)
                .where(
                    and_(
                        numbers.entity_uuid == entity_uuid,
                        numbers.sys_deleted_at == None,
                    )
                )
                .offset(offset=offset)
                .limit(limit=limit)
            )

            return statement

        @staticmethod
        def sel_num_by_entity_ct(entity_uuid: UUID4):
            numbers = NumbersModels.numbers
            statement = (
                Select(func.count())
                .select_from(numbers)
                .where(
                    and_(
                        numbers.entity_uuid == entity_uuid,
                        numbers.sys_deleted_at == None,
                    )
                )
            )

            return statement

        @staticmethod
        def sel_num_by_ent_num(
            entity_uuid: Optional[UUID4],
            country_code: Optional[str],
            area_code: Optional[str],
            line_number: Optional[str],
            ext: Optional[str],
        ):
            numbers = NumbersModels.numbers
            statement = Select(numbers).where(
                and_(
                    numbers.entity_uuid == entity_uuid,
                    numbers.country_code == country_code,
                    numbers.area_code == area_code,
                    numbers.line_number == line_number,
                    numbers.extension == ext,
                    numbers.sys_deleted_at == None,
                )
            )

            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_ent_num_uuid(
            entity_uuid: UUID4, number_uuid: UUID4, number_data: object
        ):
            numbers = NumbersModels.numbers
            statement = (
                update(numbers)
                .where(
                    and_(
                        numbers.entity_uuid == entity_uuid,
                        numbers.uuid == number_uuid,
                        numbers.sys_deleted_at == None,
                    )
                )
                .values(di.set_empty_strs_null(number_data))
                .returning(numbers)
            )
            return statement


class NumbersServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_number(
            self,
            entity_uuid: UUID4,
            number_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):

            statement = NumbersStatements.SelStatements.sel_num_by_uuid(
                entity_uuid=entity_uuid,
                number_uuid=number_uuid,
            )
            number = await Operations.return_one_row(
                service=cnst.NUMBERS_READ_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=number, exception=NumbersNotExist)

        async def get_numbers(
            self,
            entity_uuid: UUID4,
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):

            statement = NumbersStatements.SelStatements.sel_num_by_entity(
                entity_uuid=entity_uuid, limit=limit, offset=offset
            )
            numbers = await Operations.return_all_rows(
                service=cnst.NUMBERS_READ_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=numbers, exception=NumbersNotExist)

        async def get_numbers_ct(
            self,
            entity_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):

            statement = NumbersStatements.SelStatements.sel_num_by_entity_ct(
                entity_uuid=entity_uuid
            )
            return await Operations.return_count(
                service=cnst.NUMBERS_READ_SERVICE, statement=statement, db=db
            )

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_num(
            self,
            entity_uuid: UUID4,
            number_data: s_numbers.NumbersCreate,
            db: AsyncSession = Depends(get_db),
        ):
            numbers = NumbersModels.numbers
            statement = NumbersStatements.SelStatements.sel_num_by_ent_num(
                entity_uuid=entity_uuid,
                country_code=number_data.country_code,
                area_code=number_data.area_code,
                line_number=number_data.line_number,
                ext=number_data.extension,
            )
            number_exists = await Operations.return_one_row(
                service=cnst.NUMBERS_CREATE_SERVICE, statement=statement, db=db
            )
            di.record_exists(instance=number_exists, exception=NumberExists)
            number = await Operations.add_instance(
                service=cnst.NUMBERS_CREATE_SERVICE,
                model=numbers,
                data=number_data,
                db=db,
            )
            return di.record_not_exist(instance=number, exception=NumbersNotExist)

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_num(
            self,
            entity_uuid: UUID4,
            number_uuid: UUID4,
            number_data: s_numbers.NumbersUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = NumbersStatements.UpdateStatements.update_ent_num_uuid(
                entity_uuid=entity_uuid,
                number_uuid=number_uuid,
                number_data=number_data,
            )
            number = await Operations.return_one_row(
                service=cnst.NUMBERS_UPDATE_SERVICE, statement=statement, db=db
            )
            return di.record_not_exist(instance=number, exception=NumbersNotExist)

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_num_eng(
            self,
            entity_uuid: UUID4,
            number_uuid: UUID4,
            number_data: s_numbers.NumbersDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = NumbersStatements.UpdateStatements.update_ent_num_uuid(
                entity_uuid=entity_uuid,
                number_uuid=number_uuid,
                number_data=number_data,
            )
            number = await Operations.return_one_row(
                service=cnst.NUMBERS_DEL_SERVICE,
                statement=statement,
                db=db,
            )
            return di.record_not_exist(instance=number, exception=NumbersNotExist)
