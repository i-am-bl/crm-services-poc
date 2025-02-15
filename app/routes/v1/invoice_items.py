from typing import List, Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.services import container as service_container
from ...database.database import get_db, transaction_manager
from ...exceptions import InvoiceItemExists, InvoiceItemNotExist
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...schemas.invoice_items import (
    InvoiceItemsCreate,
    InvoiceItemsDel,
    InvoiceItemsInternalCreate,
    InvoiceItemsPgRes,
    InvoiceItemsUpdate,
    InvoiceItemsRes,
)
from ...services.invoice_items import CreateSrvc, ReadSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session
from ...utilities.data import internal_schema_validation

router = APIRouter()


@router.get(
    "/{invoice_uuid}/invoice-items/{invoice_item_uuid}/",
    response_model=InvoiceItemsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([InvoiceItemNotExist])
async def get_invoice_item(
    response: Response,
    invoice_uuid: UUID4,
    invoice_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    invoice_items_read_srvc: ReadSrvc = Depends(
        service_container["invoice_items_read"]
    ),
) -> InvoiceItemsRes:
    """
    Get one invoice item.
    """

    async with transaction_manager(db=db):
        return await invoice_items_read_srvc.get_invoice_item(
            invoice_uuid=invoice_uuid, invoice_item_uuid=invoice_item_uuid, db=db
        )


@router.get(
    "/{invoice_uuid}/invoice-items/",
    response_model=InvoiceItemsPgRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@set_auth_cookie
@handle_exceptions([InvoiceItemNotExist])
async def get_invoice_items(
    response: Response,
    invoice_uuid: UUID4,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    invoice_items_read_srvc: ReadSrvc = Depends(
        service_container["invoice_items_read"]
    ),
) -> InvoiceItemsPgRes:
    """
    Get invoice items by invoice.
    """

    async with transaction_manager(db=db):
        return await invoice_items_read_srvc.paginated_invoice_items(
            invoice_uuid=invoice_uuid, page=page, limit=limit, db=db
        )


@router.post(
    "/{invoice_uuid}/invoice-items/",
    response_model=List[InvoiceItemsRes],
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([InvoiceItemNotExist, InvoiceItemExists])
async def create_invoice_item(
    response: Response,
    invoice_uuid: UUID4,
    invoice_item_data: List[InvoiceItemsCreate],
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    invoice_items_create_srvc: CreateSrvc = Depends(
        service_container["invoice_items_create"]
    ),
) -> List[InvoiceItemsRes]:
    """
    Create one invoice item.
    """
    sys_user, _ = user_token
    _invoice_item_data: InvoiceItemsInternalCreate = internal_schema_validation(
        data=invoice_item_data,
        schema=InvoiceItemsInternalCreate,
        setter_method=sys_values.sys_created_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await invoice_items_create_srvc.create_invoice_item(
            invoice_uuid=invoice_uuid, invoice_item_data=_invoice_item_data, db=db
        )


# There is no need for this.
# TODO: Remove if there is no future need for this.
@router.put(
    "/{invoice_uuid}/invoice-items/{invoice_item_uuid}/",
    response_model=InvoiceItemsRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    deprecated=True,
)
@set_auth_cookie
@handle_exceptions([InvoiceItemNotExist])
async def update_invoice_item(
    response: Response,
    invoice_uuid: UUID4,
    invoice_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    invoice_items_update_srvc: UpdateSrvc = Depends(
        service_container["invoice_items_update"]
    ),
) -> InvoiceItemsRes:
    """
    Update one invoice item.
    """
    sys_user, _ = user_token
    _invoice_item_data: InvoiceItemsUpdate = internal_schema_validation(
        schema=InvoiceItemsUpdate,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )

    async with transaction_manager(db=db):
        return await invoice_items_update_srvc.update_invoice_item(
            invoice_uuid=invoice_uuid,
            invoice_item_uuid=invoice_item_uuid,
            invoice_item_data=_invoice_item_data,
            db=db,
        )


@router.delete(
    "/{invoice_uuid}/invoice-items/{invoice_item_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions([InvoiceItemNotExist])
async def soft_del_invoice_item(
    response: Response,
    invoice_uuid: UUID4,
    invoice_item_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    invoice_items_delete_srvc: DelSrvc = Depends(
        service_container["invoice_items_delete"]
    ),
) -> None:
    """
    Soft del one invoice items.
    """
    sys_user, _ = user_token
    _invoice_item_data: InvoiceItemsDel = internal_schema_validation(
        schema=InvoiceItemsDel,
        setter_method=sys_values.sys_deleted_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):
        return await invoice_items_delete_srvc.soft_del_invoice_item(
            invoice_uuid=invoice_uuid,
            invoice_item_uuid=invoice_item_uuid,
            invoice_item_data=_invoice_item_data,
            db=db,
        )
