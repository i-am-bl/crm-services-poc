from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as service_container
from ...database.database import get_db, transaction_manager
from ...exceptions import InvoiceExists, InvoiceNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.invoices import (
    InvoicesCreate,
    InvoicesInternalCreate,
    InvoicesInternalUpdate,
    InvoicesRes,
    InvoicesUpdate,
    InvoicesDel,
    InvoicesPgRes,
)
from ...services.invoices import ReadSrvc, CreateSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session
from ...utilities.data import internal_schema_validation

router = APIRouter()


@router.get(
    "/{invoice_uuid}/",
    response_model=InvoicesRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([InvoiceNotExist])
async def get_invoice(
    response: Response,
    invoice_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    invoices_read_srvc: ReadSrvc = Depends(service_container["invoices_read"]),
) -> InvoicesRes:
    """
    Get one invoice.
    """

    async with transaction_manager(db=db):
        return await invoices_read_srvc.get_invoice(invoice_uuid=invoice_uuid, db=db)


@router.get(
    "/",
    response_model=InvoicesPgRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([InvoiceNotExist])
async def get_invoices(
    response: Response,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    invoices_read_srvc: ReadSrvc = Depends(service_container["invoices_read"]),
) -> InvoicesPgRes:
    """
    Get many inovices.
    """

    async with transaction_manager(db=db):
        return await invoices_read_srvc.paginated_invoices(
            page=page, limit=limit, db=db
        )


@router.post(
    "/",
    response_model=InvoicesRes,
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([InvoiceNotExist, InvoiceExists])
async def create_invoice(
    response: Response,
    invoice_data: InvoicesCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    invoices_create_srvcs: CreateSrvc = Depends(service_container["invoices_create"]),
) -> InvoicesRes:
    """
    Create one invoice.
    """

    sys_user, _ = user_token
    _invoice_data: InvoicesInternalCreate = internal_schema_validation(
        data=invoice_data,
        schema=InvoicesInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await invoices_create_srvcs.create_invoice(
            invoice_data=_invoice_data, db=db
        )


@router.put(
    "/{invoice_uuid}/",
    response_model=InvoicesRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([InvoiceNotExist])
async def update_invoice(
    response: Response,
    invoice_uuid: UUID4,
    invoice_data: InvoicesUpdate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    invoices_update_srvc: UpdateSrvc = Depends(service_container["invoices_update"]),
) -> InvoicesRes:
    """
    Update one invoice.
    """

    sys_user, _ = user_token
    _invoice_data: InvoicesInternalUpdate = internal_schema_validation(
        data=invoice_data,
        schema=InvoicesInternalUpdate,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await invoices_update_srvc.update_invoice(
            invoice_uuid=invoice_uuid, invoice_data=_invoice_data, db=db
        )


@router.delete(
    "/{invoice_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([InvoiceNotExist])
async def soft_del_invoice(
    response: Response,
    invoice_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    invoices_delete_srvc: DelSrvc = Depends(service_container["invoices_delete"]),
) -> None:
    """
    Soft delete one invoice.
    """
    sys_user, _ = user_token
    _invoice_data: InvoicesDel = internal_schema_validation(
        schema=InvoicesDel,
        setter_method=sys_values.sys_deleted_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await invoices_delete_srvc.soft_del_invoice(
            invoice_uuid=invoice_uuid, invoice_data=_invoice_data, db=db
        )
