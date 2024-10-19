from typing import List

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import InvoiceItemExists, InvoiceItemNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import invoice_items as s_invoice_Items
from ...services.authetication import SessionService, TokenService
from ...services.invoice_items import InvoiceItemsServices
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_ivoice_items_r = InvoiceItemsServices.ReadService()
serv_ivoice_items_c = InvoiceItemsServices.CreateService()
serv_ivoice_items_u = InvoiceItemsServices.UpdateService()
serv_ivoice_items_d = InvoiceItemsServices.DelService()
serv_session = SessionService()
serv_token = TokenService()

router = APIRouter()


@router.get(
    "/v1/order-management/invoices/{invoice_uuid}/invoice-items/{invoice_item_uuid}/",
    response_model=s_invoice_Items.InvoiceItemsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([InvoiceItemNotExist])
async def get_invoice_item(
    response: Response,
    invoice_uuid: UUID4,
    invoice_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_invoice_Items.InvoiceItemsResponse:
    """get one invoice item"""

    async with transaction_manager(db=db):
        invoice_item = await serv_ivoice_items_r.get_invoice_item(
            invoice_uuid=invoice_uuid, invoice_item_uuid=invoice_item_uuid, db=db
        )
        return invoice_item


@router.get(
    "/v1/order-management/invoices/{invoice_uuid}/invoice-items/",
    response_model=s_invoice_Items.InvoiceItemsPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([InvoiceItemNotExist])
async def get_invoice_items(
    response: Response,
    invoice_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_invoice_Items.InvoiceItemsPagResponse:
    """get invoice items by invoice"""

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_ivoice_items_r.get_invoices_items_ct(
            invoice_uuid=invoice_uuid, db=db
        )
        invoice_items = await serv_ivoice_items_r.get_invoices_items(
            invoice_uuid=invoice_uuid, limit=limit, offset=offset, db=db
        )
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": pg.has_more(total_count=total_count, page=page, limit=limit),
            "invoice_items": invoice_items,
        }


@router.post(
    "/v1/order-management/invoices/{invoice_uuid}/invoice-items/",
    response_model=List[s_invoice_Items.InvoiceItemsResponse],
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([InvoiceItemNotExist, InvoiceItemExists])
async def create_invoice_item(
    response: Response,
    invoice_uuid: UUID4,
    invoice_item_data: List[s_invoice_Items.InvoiceItemsCreate],
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> List[s_invoice_Items.InvoiceItemsResponse]:
    """create one invoice item"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by_ls(data=invoice_item_data, sys_user=sys_user)
        invoice_item = await serv_ivoice_items_c.create_invoice_item(
            invoice_uuid=invoice_uuid, invoice_item_data=invoice_item_data, db=db
        )
        return invoice_item


@router.put(
    "/v1/order-management/invoices/{invoice_uuid}/invoice-items/{invoice_item_uuid}/",
    response_model=s_invoice_Items.InvoiceItemsResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([InvoiceItemNotExist])
async def update_invoice_item(
    response: Response,
    invoice_uuid: UUID4,
    invoice_item_uuid: UUID4,
    invoice_item_data: s_invoice_Items.InvoiceItemsUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_invoice_Items.InvoiceItemsResponse:
    """update one invoice item"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=invoice_item_data, sys_user=sys_user)
        invoice_item = await serv_ivoice_items_u.update_invoice_item(
            invoice_uuid=invoice_uuid,
            invoice_item_uuid=invoice_item_uuid,
            invoice_item_data=invoice_item_data,
            db=db,
        )
        return invoice_item


@router.delete(
    "/v1/order-management/invoices/{invoice_uuid}/invoice-items/{invoice_item_uuid}/",
    response_model=s_invoice_Items.InvoiceItemsDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([InvoiceItemNotExist])
async def soft_del_invoice_item(
    response: Response,
    invoice_uuid: UUID4,
    invoice_item_uuid: UUID4,
    invoice_item_data: s_invoice_Items.InvoiceItemsDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_invoice_Items.InvoiceItemsDelResponse:
    """soft del one invoice item"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=invoice_item_data, sys_user=sys_user)
        invoice_item = await serv_ivoice_items_d.soft_del_invoice_item(
            invoice_uuid=invoice_uuid,
            invoice_item_uuid=invoice_item_uuid,
            invoice_item_data=invoice_item_data,
            db=db,
        )
        return invoice_item
