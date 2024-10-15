from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy import Select, and_, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

import app.constants as cnst
import app.models.invoice_items as m_invoice_items
import app.schemas.invoice_items as s_invoice_Items
from app.database.database import Operations, get_db
from app.services.utilities import DataUtils as di


class InvoiceItemsModels:
    invoice_items = m_invoice_items.InvoiceItems


class InvoiceItemsStatements:
    pass

    class SelStatements:
        pass

        @staticmethod
        def sel_ii_by_invoice(invoice_uuid: UUID4, limit: int, offset: int):
            invoice_items = InvoiceItemsModels.invoice_items
            statement = (
                Select(invoice_items)
                .where(
                    and_(
                        invoice_items.invoice_uuid == invoice_uuid,
                        invoice_items.sys_deleted_at == None,
                    )
                )
                .offset(offset=offset)
                .limit(limit=limit)
            )
            return statement

        @staticmethod
        def sel_ii_by_invoice_ct(invoice_uuid: UUID4):
            invoice_items = InvoiceItemsModels.invoice_items
            statement = (
                Select(func.count())
                .select_from(invoice_items)
                .where(
                    and_(
                        invoice_items.invoice_uuid == invoice_uuid,
                        invoice_items.sys_deleted_at == None,
                    )
                )
            )
            return statement

        @staticmethod
        def sel_ii_by_uuid(invoice_uuid: UUID4, invoice_item_uuid: UUID4):
            invoice_items = InvoiceItemsModels.invoice_items
            statement = Select(invoice_items).where(
                and_(
                    invoice_items.invoice_uuid == invoice_uuid,
                    invoice_items.uuid == invoice_item_uuid,
                )
            )
            return statement

    class UpdateStatements:
        pass

        @staticmethod
        def update_ii_by_uuid(
            invoice_uuid: UUID4, invoice_item_uuid: UUID4, invoice_item_data: object
        ):
            invoice_items = InvoiceItemsModels.invoice_items
            statement = (
                update(invoice_items)
                .where(
                    and_(
                        invoice_items.invoice_uuid == invoice_uuid,
                        invoice_items.uuid == invoice_item_uuid,
                        invoice_items.sys_deleted_at == None,
                    )
                )
                .values(di.set_empty_strs_null(values=invoice_item_data))
                .returning(invoice_items)
            )
            return statement


class InvoiceItemsServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_invoice_item(
            self,
            invoice_uuid: UUID4,
            invoice_item_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = InvoiceItemsStatements.SelStatements.sel_ii_by_uuid(
                invoice_uuid=invoice_uuid, invoice_item_uuid=invoice_item_uuid
            )
            invoice_item = await Operations.return_one_row(
                service=cnst.INVOICE_ITEMS_READ_SERV, statement=statement, db=db
            )
            di.record_not_exist(model=invoice_item)
            return invoice_item

        async def get_invoices_items(
            self,
            invoice_uuid: UUID4,
            limit: int,
            offset: int,
            db: AsyncSession = Depends(get_db),
        ):
            statement = InvoiceItemsStatements.SelStatements.sel_ii_by_invoice(
                invoice_uuid=invoice_uuid, limit=limit, offset=offset
            )
            invoice_items = await Operations.return_all_rows(
                cnst.INVOICE_ITEMS_READ_SERV, statement=statement, db=db
            )
            di.record_not_exist(model=invoice_items)
            return invoice_items

        async def get_invoices_items_ct(
            self,
            invoice_uuid: UUID4,
            db: AsyncSession = Depends(get_db),
        ):
            statement = InvoiceItemsStatements.SelStatements.sel_ii_by_invoice_ct(
                invoice_uuid=invoice_uuid
            )
            invoice_items = await Operations.return_count(
                cnst.INVOICE_ITEMS_READ_SERV, statement=statement, db=db
            )
            di.record_not_exist(model=invoice_items)
            return invoice_items

    class CreateService:
        def __init__(self) -> None:
            pass

        async def create_invoice_item(
            self,
            invoice_uuid: UUID4,
            invoice_item_data: s_invoice_Items.InvoiceItemsCreate,
            db: AsyncSession = Depends(get_db),
        ):
            invoice_items = InvoiceItemsModels.invoice_items
            invoice_item = await Operations.add_instances(
                service=cnst.INVOICE_ITEMS_CREATE_SERV,
                model=invoice_items,
                data=invoice_item_data,
                db=db,
            )
            di.record_not_exist(model=invoice_item)
            return invoice_item

    class UpdateService:
        def __init__(self) -> None:
            pass

        async def update_invoice_item(
            self,
            invoice_uuid: UUID4,
            invoice_item_uuid: UUID4,
            invoice_item_data: s_invoice_Items.InvoiceItemsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = InvoiceItemsStatements.UpdateStatements.update_ii_by_uuid(
                invoice_uuid=invoice_uuid,
                invoice_item_uuid=invoice_item_uuid,
                invoice_item_data=invoice_item_data,
            )
            invoice_item = await Operations.return_one_row(
                cnst.INVOICE_ITEMS_UPDATE_SERV, statement=statement, db=db
            )
            di.rec_not_exist_or_soft_del(model=invoice_item)
            return invoice_item

    class DelService:
        def __init__(self) -> None:
            pass

        async def soft_del_invoice_item(
            self,
            invoice_uuid: UUID4,
            invoice_item_uuid: UUID4,
            invoice_item_data: s_invoice_Items.InvoiceItemsUpdate,
            db: AsyncSession = Depends(get_db),
        ):
            statement = InvoiceItemsStatements.UpdateStatements.update_ii_by_uuid(
                invoice_uuid=invoice_uuid,
                invoice_item_uuid=invoice_item_uuid,
                invoice_item_data=invoice_item_data,
            )
            invoice_item = await Operations.return_one_row(
                cnst.INVOICE_ITEMS_DEL_SERV, statement=statement, db=db
            )
            di.record_not_exist(model=invoice_item)
            return invoice_item
