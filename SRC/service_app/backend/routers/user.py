from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from repository import queries, models
from db import Store
import structlog
from pydantic import BaseModel

logger = structlog.get_logger(module=__name__)

User = models.User
router = APIRouter()


class CreateUserResponse(BaseModel):
    message: str
    user: User


@router.post("/user", response_model=CreateUserResponse)
async def create_user(store: Store, input: queries.CreateUserParams) -> User:
    """
    Create a new user.
    """
    try:
        # username: models.Username = await assign_username(store)
        result = await store.create_user(queries.CreateUserParams(
            sub=input.sub,
            # username=username.username,
            email=input.email,
            first_name=input.first_name,
            last_name=input.last_name,
            birthdate=input.birthdate
        ))
        assert isinstance(result, models.User)
    except IntegrityError as err:
        logger.warning(f"action blocked by database integrity error: {err}")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return CreateUserResponse(
        message="User created successfully",
        user=result
    )


@router.get("/user/{sub}", status_code=status.HTTP_200_OK)
async def get_user(store: Store, sub: str) -> User:
    try:
        result = await store.get_user_by_sub(sub=sub)
        assert isinstance(result, models.User)
        return result
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
