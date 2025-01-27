from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values


from ..models.account_lists import AccountLists
from ..utilities.utilities import DataUtils as di


class AccountListsStms:
    """
    A class responsible for constructing SQLAlchemy queries and statements for managing account lists.

    ivars:
    ivar: _account_lists: AccountLists An instance of AccountLists
    """

    def __init__(self, model: AccountLists):
        self._account_list = model
        """
        Initializes the AccountListsStms class.

        :param model: AccountLists: An instance of the AccountLists class.
        :return None
        """

    @property
    def account_list(self):
        """
        A property that returns the AccountLists model instance.

        :return: AccountLists: The instance of the AccountLists model.
        """
        return self._account_list

    def get_account_list(self, account_uuid: UUID4, account_list_uuid: UUID4):
        """
        Constructs a SQLAlchemy `Select` query to retrieve a specific account list by the account UUID.

        :param account_uuid: UUID4: The UUID of the account.
        :param account_list_uuid: UUID4: The UUID of the account list.
        :return: Select: A SQLAlchemy `Select` query to fetch the account list.
        """
        account_lists = self._account_list
        return Select(account_lists).where(
            and_(
                account_lists.account_uuid == account_uuid,
                account_lists.uuid == account_list_uuid,
                account_lists.sys_deleted_at == None,
            )
        )

    def get_account_lists_account(
        self, account_uuid: UUID4, limit: int, offset: int
    ) -> Select:
        account_lists = self._account_list
        return (
            Select(account_lists)
            .where(
                and_(
                    account_lists.account_uuid == account_uuid,
                    account_lists.sys_deleted_at == None,
                )
            )
            .offset(offset=offset)
            .limit(limit=limit)
        )

    def get_account_list_count(self, account_uuid: UUID4) -> Select:
        account_lists = self._account_list
        return (
            Select(func.count())
            .select_from(account_lists)
            .where(
                and_(
                    account_lists.account_uuid == account_uuid,
                    account_lists.sys_deleted_at == None,
                )
            )
        )

    def get_account_lists_product_list(
        self, account_uuid: UUID4, product_list_uuid: UUID4
    ) -> Select:
        account_lists = self._account_list
        return Select(account_lists).where(
            and_(
                account_lists.account_uuid == account_uuid,
                account_lists.product_list_uuid == product_list_uuid,
                account_lists.sys_deleted_at == None,
            )
        )

    def update_account_list(
        self, account_uuid: UUID4, account_list_uuid: UUID4, account_list_data: object
    ) -> update:
        account_lists = self._account_list
        return (
            update(account_lists)
            .where(
                and_(
                    account_lists.account_uuid == account_uuid,
                    account_lists.uuid == account_list_uuid,
                    account_lists.sys_deleted_at == None,
                )
            )
            .values(di.set_empty_strs_null(values=account_list_data))
            .returning(account_lists)
        )


def account_lists_stms(model: AccountLists) -> AccountListsStms:
    return AccountListsStms(model=model)
