from fastapi import APIRouter, Depends

from app.dependencies import get_db_session

from .schema import UserCreateRequest
from .services.add_new_user import add_new_user_

router = APIRouter()
prefix = "/users"
tags = ["users"]


@router.post("")
def add_new_user(
    body: UserCreateRequest,
    session=Depends(get_db_session),
) -> UserCreateRequest :
    return add_new_user_(body, session)
