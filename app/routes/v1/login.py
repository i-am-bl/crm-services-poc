from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ...containers.auth import container as auth_container
from ...database.database import get_db, transaction_manager
from ...handlers.handler import handle_exceptions
from ...services.token import TokenSrvc

router = APIRouter()


@router.post("/")
@handle_exceptions([])
async def authenticate_sys_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    token_srvc: TokenSrvc = Depends(auth_container["token_srvc"]),
):

    async with transaction_manager(db=db):
        token = await token_srvc.create_session(form_data=form_data, db=db)
        response.set_cookie(key="jwt", value=token, httponly=True, secure=True)
        return {"message": "Successfully logged in."}
