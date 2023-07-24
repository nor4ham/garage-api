from sqlalchemy.orm import Session

from ..models import User
from ..schema import UserCreateRequest


def add_new_user_(
    body: UserCreateRequest,
    session: Session,
):

    session.add(
        User(
            username=body.username,
            password=body.password,
        )
    )
