from typing import Optional
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values

from ..models.numbers import Numbers
from ..utilities.utilities import DataUtils as di


class NumberStms:
    def __init__(self, model: Numbers):
        self._model: Numbers = model

    @property
    def model(self) -> Numbers:
        return self._model

    def get_number(self, entity_uuid: UUID4, number_uuid: UUID4) -> Select:
        numbers = self._model
        return Select(numbers).where(
            and_(
                numbers.entity_uuid == entity_uuid,
                numbers.uuid == number_uuid,
            )
        )

    def get_number_by_entity(
        self,
        entity_uuid: UUID4,
        limit: int,
        offset: int,
    ) -> Select:
        numbers = self._model
        return (
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

    def get_number_by_entity_ct(self, entity_uuid: UUID4) -> Select:
        numbers = self._model
        return (
            Select(func.count())
            .select_from(numbers)
            .where(
                and_(
                    numbers.entity_uuid == entity_uuid,
                    numbers.sys_deleted_at == None,
                )
            )
        )

    def get_number_by_number(
        self,
        entity_uuid: Optional[UUID4],
        country_code: Optional[str],
        area_code: Optional[str],
        line_number: Optional[str],
        ext: Optional[str],
    ) -> Select:
        numbers = self._model
        return Select(numbers).where(
            and_(
                numbers.entity_uuid == entity_uuid,
                numbers.country_code == country_code,
                numbers.area_code == area_code,
                numbers.line_number == line_number,
                numbers.extension == ext,
                numbers.sys_deleted_at == None,
            )
        )

    def update_number(
        self, entity_uuid: UUID4, number_uuid: UUID4, number_data: object
    ) -> update:
        numbers = self._model
        return (
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
