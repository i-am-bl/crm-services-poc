from typing import List

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import get_db, transaction_manager
from ...exceptions import InvoiceExists, InvoiceNotExist
from ...handlers.handler import handle_exceptions
from ...schemas import invoices as s_invoices
from ...services.authetication import SessionService, TokenService
from ...services.invoices import InvoicesServices
from ...utilities.sys_users import SetSys
from ...utilities.utilities import Pagination as pg

serv_invoices_r = InvoicesServices.ReadService()
serv_invoices_c = InvoicesServices.CreateService()
serv_invoices_u = InvoicesServices.UpdateService()
serv_invoices_d = InvoicesServices.DelService()
serv_session = SessionService()
serv_token = TokenService()

router = APIRouter()


@router.get(
    "/v1/order-management/invoices/{invoice_uuid}/",
    response_model=s_invoices.InvoicesResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([InvoiceNotExist])
async def get_invoice(
    response: Response,
    invoice_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_invoices.InvoicesResponse:
    """get one invoice"""

    async with transaction_manager(db=db):
        invoice = await serv_invoices_r.get_invoice(invoice_uuid=invoice_uuid, db=db)
        return invoice


@router.get(
    "/v1/order-management/invoices/",
    response_model=s_invoices.InvoicesPagResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([InvoiceNotExist])
async def get_invoices(
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_invoices.InvoicesPagResponse:
    """get many inovices"""

    async with transaction_manager(db=db):
        offset = pg.pagination_offset(page=page, limit=limit)
        total_count = await serv_invoices_r.get_invoices_ct(db=db)
        invoices = await serv_invoices_r.get_invoices(limit=limit, offset=offset, db=db)
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": pg.has_more(total_count=total_count, page=page, limit=limit),
            "invoices": invoices,
        }


@router.post(
    "/v1/order-management/invoices/",
    response_model=s_invoices.InvoicesResponse,
    status_code=status.HTTP_201_CREATED,
)
@serv_token.set_auth_cookie
@handle_exceptions([InvoiceNotExist, InvoiceExists])
async def create_invoice(
    response: Response,
    invoice_data: s_invoices.InvoicesCreate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_invoices.InvoicesResponse:
    """create on invoice"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_created_by(data=invoice_data, sys_user=sys_user)
        invoice = await serv_invoices_c.create_invoice(invoice_data=invoice_data, db=db)
        return invoice


@router.put(
    "/v1/order-management/invoices/{invoice_uuid}/",
    response_model=s_invoices.InvoicesResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([InvoiceNotExist])
async def update_invoice(
    response: Response,
    invoice_uuid: UUID4,
    invoice_data: s_invoices.InvoicesUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_invoices.InvoicesResponse:
    """update one invoice"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_updated_by(data=invoice_data, sys_user=sys_user)
        invoice = await serv_invoices_u.update_invoice(
            invoice_uuid=invoice_uuid, invoice_data=invoice_data, db=db
        )
        return invoice


@router.delete(
    "/v1/order-management/invoices/{invoice_uuid}/",
    response_model=s_invoices.InvoicesDelResponse,
    status_code=status.HTTP_200_OK,
)
@serv_token.set_auth_cookie
@handle_exceptions([InvoiceNotExist])
async def soft_del_invoice(
    response: Response,
    invoice_uuid: UUID4,
    invoice_data: s_invoices.InvoicesDel,
    db: AsyncSession = Depends(get_db),
    user_token: str = Depends(serv_session.validate_session),
) -> s_invoices.InvoicesDel:
    """soft delete one invoice"""

    async with transaction_manager(db=db):
        sys_user, _ = user_token
        SetSys.sys_deleted_by(data=invoice_data, sys_user=sys_user)
        invoice = await serv_invoices_d.soft_del_invoice(
            invoice_uuid=invoice_uuid, invoice_data=invoice_data, db=db
        )
        return invoice
