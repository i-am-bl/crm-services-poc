from typing import List

from fastapi import APIRouter, Depends, Query, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.invoices as s_invoices
from app.database.database import get_db
from app.services.invoices import InvoicesServices
from app.service_utils import pagination_offset

serv_invoices_r = InvoicesServices.ReadService()
serv_invoices_c = InvoicesServices.CreateService()
serv_invoices_u = InvoicesServices.UpdateService()
serv_invoices_d = InvoicesServices.DelService()

router = APIRouter()


@router.get(
    "/v1/order-management/invoices/{invoice_uuid}/",
    response_model=s_invoices.InvoicesResponse,
    status_code=status.HTTP_200_OK,
)
async def get_invoice(invoice_uuid: UUID4, db: AsyncSession = Depends(get_db)):
    """get one invoice"""
    async with db.begin():
        invoice = await serv_invoices_r.get_invoice(invoice_uuid=invoice_uuid, db=db)
        return invoice


@router.get(
    "/v1/order-management/invoices/",
    response_model=s_invoices.InvoicesPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_invoices(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """get many inovices"""
    async with db.begin():
        offset = pagination_offset(page=page, limit=limit)
        total_count = await serv_invoices_r.get_invoices_ct(db=db)
        invoices = await serv_invoices_r.get_invoices(limit=limit, offset=offset, db=db)
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "has_more": total_count > (page * limit),
            "invoices": invoices,
        }


@router.post(
    "/v1/order-management/invoices/",
    response_model=s_invoices.InvoicesResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_invoice(
    invoice_data: s_invoices.InvoicesCreate, db: AsyncSession = Depends(get_db)
):
    """create on invoice"""
    async with db.begin():
        invoice = await serv_invoices_c.create_invoice(invoice_data=invoice_data, db=db)
        return invoice


@router.put(
    "/v1/order-management/invoices/{invoice_uuid}/",
    response_model=s_invoices.InvoicesResponse,
    status_code=status.HTTP_200_OK,
)
async def update_invoice(
    invoice_uuid: UUID4,
    invoice_data: s_invoices.InvoicesUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one invoice"""
    async with db.begin():
        invoice = await serv_invoices_u.update_invoice(
            invoice_uuid=invoice_uuid, invoice_data=invoice_data, db=db
        )
        return invoice


@router.delete(
    "/v1/order-management/invoices/{invoice_uuid}/",
    response_model=s_invoices.InvoicesDelResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_del_invoice(
    invoice_uuid: UUID4,
    invoice_data: s_invoices.InvoicesDel,
    db: AsyncSession = Depends(get_db),
):
    """soft delete one invoice"""
    async with db.begin():
        invoice = await serv_invoices_d.soft_del_invoice(
            invoice_uuid=invoice_uuid, invoice_data=invoice_data, db=db
        )
        return invoice
