from typing import List

from fastapi import APIRouter, Depends, Query, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.invoice_items as s_invoice_Items
from app.database.database import get_db
from app.services.invoice_items import InvoiceItemsServices
from app.service_utils import pagination_offset

serv_ivoice_items_r = InvoiceItemsServices.ReadService()
serv_ivoice_items_c = InvoiceItemsServices.CreateService()
serv_ivoice_items_u = InvoiceItemsServices.UpdateService()
serv_ivoice_items_d = InvoiceItemsServices.DelService()


router = APIRouter()


@router.get(
    "/v1/order-management/invoices/{invoice_uuid}/invoice-items/{invoice_item_uuid}/",
    response_model=s_invoice_Items.InvoiceItemsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_invoice_item(
    invoice_uuid: UUID4, invoice_item_uuid: UUID4, db: AsyncSession = Depends(get_db)
):
    """get one invoice item"""
    async with db.begin():
        invoice_item = await serv_ivoice_items_r.get_invoice_item(
            invoice_uuid=invoice_uuid, invoice_item_uuid=invoice_item_uuid, db=db
        )
        return invoice_item


@router.get(
    "/v1/order-management/invoices/{invoice_uuid}/invoice-items/",
    response_model=s_invoice_Items.InvoiceItemsPagResponse,
    status_code=status.HTTP_200_OK,
)
async def get_invoice_item(
    invoice_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
):
    """get invoice items by invoice"""
    async with db.begin():
        offset = pagination_offset(page=page, limit=limit)
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
            "has_more": total_count > (page * limit),
            "invoice_items": invoice_items,
        }


@router.post(
    "/v1/order-management/invoices/{invoice_uuid}/invoice-items/",
    response_model=List[s_invoice_Items.InvoiceItemsResponse],
    status_code=status.HTTP_200_OK,
)
async def create_invoice_item(
    invoice_uuid: UUID4,
    invoice_item_data: List[s_invoice_Items.InvoiceItemsCreate],
    db: AsyncSession = Depends(get_db),
):
    """create one invoice item"""
    async with db.begin():
        invoice_item = await serv_ivoice_items_c.create_invoice_item(
            invoice_uuid=invoice_uuid, invoice_item_data=invoice_item_data, db=db
        )
        return invoice_item


@router.put(
    "/v1/order-management/invoices/{invoice_uuid}/invoice-items/{invoice_item_uuid}/",
    response_model=s_invoice_Items.InvoiceItemsResponse,
    status_code=status.HTTP_200_OK,
)
async def update_invoice_item(
    invoice_uuid: UUID4,
    invoice_item_uuid: UUID4,
    invoice_item_data: s_invoice_Items.InvoiceItemsUpdate,
    db: AsyncSession = Depends(get_db),
):
    """update one invoice item"""
    async with db.begin():
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
async def soft_del_invoice_item(
    invoice_uuid: UUID4,
    invoice_item_uuid: UUID4,
    invoice_item_data: s_invoice_Items.InvoiceItemsDel,
    db: AsyncSession = Depends(get_db),
):
    """soft del one invoice item"""
    async with db.begin():
        invoice_item = await serv_ivoice_items_d.soft_del_invoice_item(
            invoice_uuid=invoice_uuid,
            invoice_item_uuid=invoice_item_uuid,
            invoice_item_data=invoice_item_data,
            db=db,
        )
        return invoice_item
