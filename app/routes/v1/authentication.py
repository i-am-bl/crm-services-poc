from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ...constants import constants as cnst
from ...database.database import get_db
from ...services.authetication import SessionService

serv_session = SessionService()
router = APIRouter()


@router.post("/v1/system-management/login")
async def authenticate_sys_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        async with db.begin():
            token = await serv_session.create_session(form_data=form_data, db=db)
            response.set_cookie(key="jwt", value=token, httponly=True, secure=True)
            # TODO: handle this misleading message
            return {"message": "Successfully logged in."}
    except Exception as e:
        raise e
