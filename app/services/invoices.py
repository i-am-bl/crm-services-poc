from importlib import invalidate_caches
from math import e

from fastapi import Depends, status
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession


from ..models import invoices as m_invoices
from ..schemas import invoices as s_invoices
from ..constants import constants as cnst
from ..database.database import Operations, get_db
from ..utilities.utilities import DataUtils as di
from ..exceptions import InvoiceNotExist, InvoiceExists


class InvoicesModels:
    inovices = m_invoices.Invoices


class InvoicesStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_invoices_by_uuid(invoice_uuid: UUID4):
            invoices = InvoicesModels.inovices
            statement = Select(invoices).where(
                and_(invoices.uuid == invoice_uuid, invoices.sys_deleted_at == None)
            )
            return statement

        @staticmethod
        def sel_invoices_by_order(order_uuid: UUID4):
            invoices = InvoicesModels.inovices
            statement = Select(invoices).where(
                and_(
                    invoices.order_uuid == order_uuid,
                    invoices.sys_deleted_at == None,
                )
            )
            return statement

        @staticmethod
        def sel_invoices(limit: int, offset: int):
            invoices = InvoicesModels.inovices
            statement = (
                Select(invoices)
                .where(invoices.sys_deleted_at == None)
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_invoices_ct():
            invoices = InvoicesModels.inovices
            statement = (
                Select(func.count())
                .select_from(invoices)
                .where(invoices.sys_deleted_at == None)
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_invoices_by_uuid(invoice_uuid: UUID4, invoice_data: object):
            invoices = InvoicesModels.inovices
            statement = (
                update(invoices)
                .where(
                    and_(invoices.uuid == invoice_uuid, invoices.sys_deleted_at == None)
                )
                .values(di.set_empty_strs_null(values=invoice_data))
                .returning(invoices)
            )
            return statement


class InvoicesServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_invoice(
            self, invoice_uuid: UUID4, db: AsyncSession = Depends(get_db)
        ):
            statement = InvoicesStatements.SelStatements.sel_invoices_by_uuid(
                invoice_uuid=invoice_uuid
            )
            invoice = await Operations.return_one_row(
                service=cnst.INVOICES_READ_SERV, statement=statement, db=db
            )
            di.record_not_exist(instance=invoice, exception=InvoiceNotExist)
            return invoice

        async def get_invoices(
            self, limit: int, offset: int, db: AsyncSession = Depends(get_db)
        ):
            statement = InvoicesStatements.SelStatements.sel_invoices(
                limit=limit, offset=offset
            )
            invoices = await Operations.return_all_rows(
                service=cnst.INVOICES_READ_SERV, statement=statement, db=db
            )
            di.record_not_exist(instance=invoices, exception=InvoiceNotExist)
            return invoices

        async def get_invoices_ct(self, db: AsyncSession = Depends(get_db)):
            statement = InvoicesStatements.SelStatements.sel_invoices_ct()
            invoices = await Operations.return_count(
                service=cnst.INVOICES_READ_SERV, statement=statement, db=db
            )

            return invoices

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_invoice(
            self,
            invoice_data: s_invoices.InvoicesCreate,
            db: AsyncSession = Depends(get_db),
        ):
            invoices = InvoicesModels.inovices
            statement = InvoicesStatements.SelStatements.sel_invoices_by_order(
                order_uuid=invoice_data.order_uuid
            )
            invoice_exists = await Operations.return_one_row(
                service=cnst.INVOICES_CREATE_SERV, statement=statement, db=db
            )
            di.record_exists(instance=invoice_exists, exception=InvoiceExists)
            invoice = await Operations.add_instance(
                service=cnst.INVOICES_CREATE_SERV,
                model=invoices,
                data=invoice_data,
                db=db,
            )
            di.record_not_exist(instance=invoice, exception=InvoiceNotExist)
            return invoice

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_invoice(
            self,
            invoice_uuid: UUID4,
            invoice_data: s_invoices.InvoicesUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = InvoicesStatements.UpdateStatements.update_invoices_by_uuid(
                invoice_uuid=invoice_uuid, invoice_data=invoice_data
            )
            invoice = await Operations.return_one_row(
                service=cnst.INVOICES_UPDATE_SERV, statement=statement, db=db
            )
            di.record_not_exist(instance=invoice, exception=InvoiceNotExist)
            return invoice

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_invoice(
            self,
            invoice_uuid: UUID4,
            invoice_data: s_invoices.InvoicesDel,
            db: AsyncSession = Depends(get_db),
        ):
            statement = InvoicesStatements.UpdateStatements.update_invoices_by_uuid(
                invoice_uuid=invoice_uuid, invoice_data=invoice_data
            )
            invoice = await Operations.return_one_row(
                service=cnst.INVOICES_DEL_SERV, statement=statement, db=db
            )
            di.record_not_exist(instance=invoice, exception=InvoiceNotExist)
            return invoice
