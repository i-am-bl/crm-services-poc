from typing import Optional
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values, Update

from ..models.numbers import Numbers
from ..utilities.data import set_empty_strs_null


class NumbersStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing phone number records.

    ivars:
    ivar: _model: Numbers: An instance of the Numbers model.
    """

    def __init__(self, model: Numbers) -> None:
        """
        Initializes the NumberStms class.

        :param model: Numbers: An instance of the Numbers model.
        :return: None
        """
        self._model: Numbers = model

    @property
    def model(self) -> Numbers:
        """
        Returns the Numbers model.

        :return: Numbers: The Numbers model instance.
        """
        return self._model

    def get_number(self, entity_uuid: UUID4, number_uuid: UUID4) -> Select:
        """
        Selects a specific phone number by its entity UUID and number UUID.

        :param entity_uuid: UUID4: The UUID of the entity.
        :param number_uuid: UUID4: The UUID of the number.
        :return: Select: A Select statement for the specific phone number.
        """
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
        """
        Selects phone numbers by entity UUID with pagination.

        :param entity_uuid: UUID4: The UUID of the entity.
        :param limit: int: The maximum number of records to return.
        :param offset: int: The number of records to skip.
        :return: Select: A Select statement for phone numbers filtered by entity UUID with pagination.
        """
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
        """
        Selects the count of phone numbers for a given entity UUID.

        :param entity_uuid: UUID4: The UUID of the entity.
        :return: Select: A Select statement for the count of phone numbers for the given entity UUID.
        """
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
        """
        Selects a phone number by entity UUID, country code, area code, line number, and extension.

        :param entity_uuid: Optional[UUID4]: The UUID of the entity.
        :param country_code: Optional[str]: The country code of the phone number.
        :param area_code: Optional[str]: The area code of the phone number.
        :param line_number: Optional[str]: The line number of the phone number.
        :param ext: Optional[str]: The extension of the phone number.
        :return: Select: A Select statement for the specific phone number matching all criteria.
        """
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
        """
        Updates a phone number by its entity UUID and number UUID.

        :param entity_uuid: UUID4: The UUID of the entity.
        :param number_uuid: UUID4: The UUID of the phone number.
        :param number_data: object: The data to update the phone number with.
        :return: Update: An Update statement for the phone number.
        """
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
            .values(set_empty_strs_null(number_data))
            .returning(numbers)
        )
