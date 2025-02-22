from typing import Tuple

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.orchestrators import container as orchs_container
from ...containers.services import container as services_container
from ...database.database import get_db, transaction_manager
from ...exceptions import (
    EntityDataInvalid,
    EntityIndivDataInvalid,
    EntityNonIndivDataInvalid,
    EntityNotExist,
    EntityTypeInvalid,
    IndividualNotExist,
    NonIndividualNotExist,
)
from ...handlers.handler import handle_exceptions
from ...models.sys_users import SysUsers
from ...orchestrators.entities import EntitiesCreateOrch
from ...schemas.entities import (
    EntitiesDel,
    EntitiesPgRes,
    EntitiesCombinedRes,
    EntitiesRes,
    EntitiesUpdate,
)
from ...schemas.individuals import IndividualsRes, IndividualsCreate
from ...schemas.non_individuals import NonIndividualsRes, NonIndividualsCreate
from ...services.entities import ReadSrvc, UpdateSrvc, DelSrvc
from ...services.token import set_auth_cookie
from ...utilities import sys_values
from ...utilities.auth import get_validated_session
from ...utilities.data import internal_schema_validation

router = APIRouter()


@router.get(
    "/{entity_uuid}/",
    response_model=EntitiesRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([EntityNotExist])
async def get_entity(
    entity_uuid: UUID4,
    response: Response,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    entities_read_srvc: ReadSrvc = Depends(services_container["entities_read"]),
) -> EntitiesRes:
    """
    Get one entity by entity_uuid.

    """
    async with transaction_manager(db=db):
        return await entities_read_srvc.get_entity(entity_uuid=entity_uuid, db=db)


@router.get(
    "/",
    response_model=EntitiesPgRes,
    status_code=status.HTTP_200_OK,
)
@set_auth_cookie
@handle_exceptions([EntityNotExist, EntityTypeInvalid])
async def get_entities(
    response: Response,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    entities_read_srvc: ReadSrvc = Depends(services_container["entities_read"]),
) -> EntitiesPgRes:
    """
    Retrieve a list of entities.
    """
    async with transaction_manager(db=db):
        return await entities_read_srvc.paginated_entities(
            page=page, limit=limit, db=db
        )


@router.post(
    "/",
    response_model=NonIndividualsRes | IndividualsRes,
    status_code=status.HTTP_201_CREATED,
)
@set_auth_cookie
@handle_exceptions([EntityNotExist, EntityTypeInvalid])
async def create_entity(
    response: Response,
    entity_data: IndividualsCreate | NonIndividualsCreate,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    entities_creates_srvc: EntitiesCreateOrch = Depends(
        orchs_container["entities_create_orch"]
    ),
) -> NonIndividualsRes | IndividualsRes:

    sys_user, _ = user_token
    async with transaction_manager(db=db):
        return await entities_creates_srvc.create_entity(
            entity_data=entity_data, db=db, sys_user=sys_user
        )


# There is no need for this at this time.
# TODO: Remove if there no future use.
@router.put(
    "/{entity_uuid}/",
    response_model=EntitiesCombinedRes,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    deprecated=True,
)
@set_auth_cookie
@handle_exceptions(
    [
        EntityNotExist,
        IndividualNotExist,
        NonIndividualNotExist,
        EntityIndivDataInvalid,
        EntityNonIndivDataInvalid,
        EntityDataInvalid,
    ]
)
async def update_entity(
    response: Response,
    entity_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    entities_update_srvc: UpdateSrvc = Depends(services_container["entities_update"]),
) -> EntitiesCombinedRes:
    """
    Update one entity by entity_uuid.
    """
    # TODO: if type changes, the child record based on type must be deleted.
    sys_user, _ = user_token
    _entity_data: EntitiesUpdate = internal_schema_validation(
        schema=EntitiesUpdate,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):

        return await entities_update_srvc.update_entity(
            entity_uuid=entity_uuid, entity_data=_entity_data, db=db
        )


@router.delete(
    "/{entity_uuid}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
@set_auth_cookie
@handle_exceptions(
    [
        EntityNotExist,
        IndividualNotExist,
        NonIndividualNotExist,
    ]
)
async def soft_del_entity(
    response: Response,
    entity_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple[SysUsers, str] = Depends(get_validated_session),
    entities_delete_srvc: DelSrvc = Depends(services_container["entities_delete"]),
) -> None:
    """
    Soft del one entity by entity_uuid.
    """
    sys_user, _ = user_token
    _entity_data: EntitiesDel = internal_schema_validation(
        schema=EntitiesDel,
        setter_method=sys_values.sys_updated_by,
        sys_user_uuid=sys_user.uuid,
    )
    async with transaction_manager(db=db):

        await entities_delete_srvc.soft_del_entity(
            entity_uuid=entity_uuid, entity_data=_entity_data, db=db
        )
